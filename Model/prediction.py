
from abc import ABC
from csv import writer
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer
# import sys

from ts.torch_handler.base_handler import BaseHandler
class TransformersClassifierHandler(BaseHandler, ABC):
    def __init__(self):
        super(TransformersClassifierHandler, self).__init__()
        self.initialized = False

    def initialize(self):
        self.model = AutoModelForSequenceClassification.from_pretrained("./bert_models/bert_model")
        self.tokenizer = AutoTokenizer.from_pretrained("./bert_models/token_model/")

        self.model.eval()

    def preprocess(self, data):
        sentences = data

        inputs = self.tokenizer.encode_plus(
            sentences,
            add_special_tokens=True,
            return_tensors="pt"
        )
        return inputs

    def inference(self, inputs):
    
        prediction = self.model(
            inputs['input_ids'].to(self.device), 
            token_type_ids=inputs['token_type_ids'].to(self.device)
        )[0]

        if self.mapping:
            prediction = self.mapping[str(prediction)]

        return prediction

    def postprocess(self, inference_output):
        return inference_output

class_names = ["Business_Ethics","Data_Security","Access_And_Affordability"
    ,"Business_Model_Resilience"
    ,"Competitive_Behavior"
    ,"Critical_Incident_Risk_Management",
    "Customer_Welfare",
    "Director_Removal",
    "Employee_Engagement_Inclusion_And_Diversity",
    "Employee_Health_And_Safety",
    "Human_Rights_And_Community_Relations",
    "Labor_Practices",
    "Management_Of_Legal_And_Regulatory_Framework"
    ,"Physical_Impacts_Of_Climate_Change"
    ,"Product_Quality_And_Safety"
    ,"Product_Design_And_Lifecycle_Management"
    ,"Selling_Practices_And_Product_Labeling"
    ,"Supply_Chain_Management"
    ,"Systemic_Risk_Management"
    ,"Waste_And_Hazardous_Materials_Management"
    ,"Water_And_Wastewater_Management"
    ,"Air_Quality"
    ,"Customer_Privacy"
    ,"Ecological_Impacts"
    ,"Energy_Management"
    ,"GHG_Emissions"]


def predict(input):
    _service = TransformersClassifierHandler()
    def handle(data):
        _service.initialize()
        data = _service.preprocess(data)
        data = _service.inference(data)
        data = _service.postprocess(data)
        return data

    def softmax(x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    with open(input,encoding="utf-8") as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        temp = []
        temp.append(line)
        new_lines.append(temp)

    # dumping output
    with open('../outputs/classification_output.csv','w') as f:
        writer_object = writer(f)
        writer_object.writerow(["sentence","class_num","class_name"]) 
        for line in new_lines:
            try:
                probs = softmax(np.array(handle(line[0]).detach().numpy())[0])
                if(np.amax(probs)>0.25):
                    writer_object.writerow([line[0],probs.argmax(),class_names[probs.argmax()]])
                else:
                    #outlier
                    writer_object.writerow([line[0],26,"Outlier"])
            except (UnicodeEncodeError):
                continue
    f.close()
# print(type(handle("We have reduced the emissions by 50%.")))



# A = np.array(handle("Emissions Sai has got 50%").detach().numpy())
# B = softmax(A[0])
# # print(softmax([3.0, 1.0, 0.2]))
# print(A)
# print(np.amax(B))
# print(np.amax(B))
# B = np.transpose(B)
# cosine = np.dot(A,B)/(norm(A)*norm(B))
# print(cosine)
