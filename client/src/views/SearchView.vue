<template>
    <BackButton />
    <SearchUploader @submit=submitImage />
    <var-popup v-model:show="showPopup">
        <Loading v-if="isLoading" />
        <SearchResult v-if="isDisplayingResult" :canonical-name="canonicalName" />
        <OptionPanel v-if="isDisplayingOptions" :attributes="candidatesAttributes" @choice-made="makeChoice" />
    </var-popup>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import qs from 'qs';
import BackButton from '../components/BackButton.vue';
import SearchUploader from '../components/SearchUploader.vue'
import Loading from '../components/Loading.vue'
import SearchResult from '../components/SearchResult.vue';
import OptionPanel from '../components/OptionPanel.vue';

const showPopup = ref(false)
const isLoading = ref(false)
const isDisplayingResult = ref(false)
const isDisplayingOptions = ref(false)


const canonicalName = ref("")
const candidatesAttributes = ref({})
const candidatesAndProbs = ref({})
const choiceCount = ref(0)



function submitImage(file) {
    showPopup.value = true
    isDisplayingResult.value = false
    isLoading.value = true

    const formData = new FormData()
    formData.append('file', file.file);
    axios.post("http://localhost:8080/uploadImage", formData, {
        headers: { "Content-Type": "multipart/form-data" }
    }).then((response) => {
        console.log(response.data)
        candidatesAndProbs.value = response.data
        if (Object.keys(candidatesAndProbs.value).length === 1) {
            // 如果返回的是确定的结果，则直接展示
            canonicalName.value = Object.keys(candidatesAndProbs.value)[0]
            isLoading.value = false
            isDisplayingOptions.value = false
            isDisplayingResult.value = true
        } else {
            // 如果返回了多个候选结果，比较其属性并对用户提出问题
            candidatesAndProbs.value = filterCandidates(candidatesAndProbs.value)

            axios.get("http://localhost:8080//integrateInformation", {
                params: {
                    candidates: Object.keys(candidatesAndProbs.value),
                }, paramsSerializer: {
                    serialize: function (params) {
                        return qs.stringify(params, { arrayFormat: 'repeat' })
                    }
                },
            }).then(
                (response) => {
                    candidatesAttributes.value = response.data
                    isLoading.value = false
                    isDisplayingOptions.value = true
                }
            )
        }
    })
}

function changeProbs(canonicalName) {
    candidatesAndProbs.value[canonicalName] *= 1.5
}

function checkWinner() {
    // 检查是否已经有满足条件的候选者
    let candidatesList = []
    for (let candidate in candidatesAndProbs.value) {
        candidatesList.push({ name: candidate, prob: candidatesAndProbs.value[candidate] })
    }
    candidatesList.sort(function (a, b) { return b.prob - a.prob })
    for (let candidate in candidatesList.slice(1)) {
        if (candidatesList.slice(1)[candidate].prob / candidatesList[0].prob > 0.3) {
            return null
        }
    }
    return candidatesList[0].name
}

function makeChoice(name) {
    // 如果选择了具体的选项，检查是否已经产生了达到要求的候选植物
    if (name !== null) {
        changeProbs(name)
        let winner = checkWinner()
        if (winner !== null) {
            choiceCount.value = 0
            canonicalName.value = winner
            isDisplayingOptions.value = false
            isDisplayingResult.value = true
        }
    }

    choiceCount.value++

    // 如果所有属性都选完了，取置信度最高的候选植物
    if (choiceCount.value === Object.keys(candidatesAttributes.value).length && isDisplayingOptions.value === true) {
        choiceCount.value = 0
        let candidatesList = []
        for (let candidate in candidatesAndProbs.value) {
            candidatesList.push({ name: candidate, prob: candidatesAndProbs.value[candidate] })
        }
        candidatesList.sort(function (a, b) { return b.prob - a.prob })
        canonicalName.value = candidatesList[0].name
        isDisplayingOptions.value = false
        isDisplayingResult.value = true

    }
}

function filterCandidates(candidatesAndProbs) {
    // 仅保留置信度前三的候选植物
    let candidatesList = []
    for (let candidate in candidatesAndProbs) {
        candidatesList.push({ name: candidate, prob: candidatesAndProbs[candidate] })
    }
    candidatesList.sort(function (a, b) { return b.prob - a.prob })
    candidatesList = candidatesList.slice(0, Math.min(candidatesList.length, 3))

    let filteredCandidatesAndProbs = {}
    for (let index in candidatesList) {
        filteredCandidatesAndProbs[candidatesList[index].name] = candidatesList[index].prob
    }
    return filteredCandidatesAndProbs
}

</script>
