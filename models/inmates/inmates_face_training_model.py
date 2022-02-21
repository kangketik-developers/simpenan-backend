from pydantic import BaseModel

class FaceTrainingOut(BaseModel):
    acc: float
    val_acc: float
    loss: float
    val_loss: float