# BotanyPedia

## Requirements
> python == 3.10
>
> npm
>
> neo4j

Install python dependencies.
```bash
pip install -r requirements.txt
```

## Build graph
You should first have your data (plant info, attribute, etc.) stored in `./build_graph`.
```bash
cd build_graph
python main.py
```

**_TODO: data format_**

## Run App
Run BotanyPedia for development.
```bash
# client
cd client
npm run dev -- --port 80 # or any other port you prefer

#server
cd server
flask run --port=8080 # server must be listen on port 8080
```