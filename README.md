# ML
1. `cd src`
2.  `pip3 install --no-cache-dir -r requirements.txt`
3.  `uvicorn app.api:app --host 0.0.0.0 --port 8002 --reload --reload-dir ./app --access-log`
4. Access `http://localhost:8002/ml/v1/docs`
