from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI()

model = joblib.load("./model.joblib")

class PredictionRequest(BaseModel):
    features: list

# TEST BODY: ["90", "RL", 65.0, 8944.0, "Reg", "Lvl", "Inside", "Gtl", "NAmes", "Duplex", "1Story", 5, 5, 1967.0, 1967.0, "Gable", "None", 0.0, "TA", "TA", "CBlock", "TA", "TA", "No", "Unf", 0.0, "Unf", 0.0, 1584.0, 1584.0, "TA", "Y", "SBrkr", 1584.0, 0.0, 0.0, 1584.0, 0.0, 0.0, 2.0, 0.0, 4.0, 2.0, "TA", 8.0, "Mod", 0.0, "Detchd", "Unf", 3.0, 792.0, "Y", 0.0, 152.0, 0.0, 0.0, 0.0, 0.0, "NoFence", 0.0, 4.0, 2009.0, "GroupedWD", "Normal", "Norm", false, false, "Plywood", 42.0, 1]  

columns = ['MS.SubClass', 'MS.Zoning', 'Lot.Frontage', 'Lot.Area', 'Lot.Shape', 'Land.Contour', 'Lot.Config', 'Land.Slope', 'Neighborhood', 'Bldg.Type', 'House.Style', 'Overall.Qual', 'Overall.Cond', 'Year.Built', 'Year.Remod.Add', 'Roof.Style', 'Mas.Vnr.Type', 'Mas.Vnr.Area', 'Exter.Qual', 'Exter.Cond', 'Foundation', 'Bsmt.Qual', 'Bsmt.Cond', 'Bsmt.Exposure', 'BsmtFin.Type.1', 'BsmtFin.SF.1', 'BsmtFin.Type.2', 'BsmtFin.SF.2', 'Bsmt.Unf.SF', 'Total.Bsmt.SF', 'Heating.QC', 'Central.Air', 'Electrical', 'X1st.Flr.SF', 'X2nd.Flr.SF', 'Low.Qual.Fin.SF', 'Gr.Liv.Area', 'Bsmt.Full.Bath', 'Bsmt.Half.Bath', 'Full.Bath', 'Half.Bath', 'Bedroom.AbvGr', 'Kitchen.AbvGr', 'Kitchen.Qual', 'TotRms.AbvGrd', 'Functional', 'Fireplaces', 'Garage.Type', 'Garage.Finish', 'Garage.Cars', 'Garage.Area', 'Paved.Drive', 'Wood.Deck.SF', 'Open.Porch.SF', 'Enclosed.Porch', 'X3Ssn.Porch', 'Screen.Porch', 'Pool.Area', 'Fence', 'Misc.Val', 'Mo.Sold', 'Yr.Sold', 'Sale.Type', 'Sale.Condition', 'SalePrice', 'Condition', 'HasShed', 'HasAlley', 'Exterior', 'Garage.Age']

@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        features = pd.DataFrame([request.features], columns=columns)
        prediction = model.predict(features)

        return { "result": prediction[0] }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)

