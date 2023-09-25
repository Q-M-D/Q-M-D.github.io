import os

# run aws s3 sync _site s3://open-em

os.system("aws s3 sync _site s3://open-em")
print("aws s3 sync _site s3://open-em")