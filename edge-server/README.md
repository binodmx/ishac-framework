1. Install python packages
    - pip install web3
    - pip install py-solc-x
2. Set environment variables in `.env`
3. Run the flask app using `python -m flask run`

> Use *git bash terminal* for following commands.

4. Check health `curl http://localhost:5000`
5. Get attribute
    - `curl -X POST http://localhost:5000/validate -H "Content-type: application/json" -d "{}"`
    - `curl -X POST http://localhost:5000/validate -H "Content-type: application/json" -d @data.json`
