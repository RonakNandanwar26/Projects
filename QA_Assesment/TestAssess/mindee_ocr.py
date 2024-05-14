# from mindee import Client, product

key = '5b75f382b99074f8698e4152cc4b38bc'
# # Init a new client
# mindee_client = Client(api_key=key)

# # Load a file from disk
# input_doc = mindee_client.source_from_path("C:/Users/Albiorix Technology/Desktop/Ronak/Projects/QA_Assesment/educator.pdf")
# my_endpoint = mindee_client.create_endpoint(
#     endpoint_name="pdf",
#     account_name="ronak",
#     version="v1",
# )

# # Parse the document as an invoice by passing the appropriate type
# result = mindee_client.parse(
#     product.CustomV1,
#     input_doc,
#     endpoint=my_endpoint
# )

# # Print a brief summary of the parsed data
# print(result.document)


from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key=key)

# Load a file from disk
input_doc = mindee_client.source_from_path(r'C:\Users\Albiorix Technology\Desktop\Ronak\Projects\QA_Assesment\educator.pdf')

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.us.W9V1, input_doc)

# Print a brief summary of the parsed data
print(result.document)

# # Iterate over all the fields in the document
# for field_name, field_values in result.document.inference.prediction.fields.items():
#     print(field_name, "=", field_values)