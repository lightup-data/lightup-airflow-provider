# Airflow Provider for Lightup

# Airflow configuration 

Go to Admin > Connections and add connection:
![image](https://user-images.githubusercontent.com/107838279/228045709-4858aabc-c3f3-40a3-aae0-b8fa293cb58e.png)

Put refresh token (https://docs.lightup.ai/reference/post_api-v1-token-refresh) into Password section, and save.

# Operators

**LightupTriggerOperator**: Triggers the Lightup platform based on configuration to collect metrics and evaluate them.

# Sensors

**LightupTriggerResultSensor**: Connects to the Lightup platform and checks the progress of the trigger operator. Returns when the trigger operation has been processed by the platform. Once the sensor returns, results can be pulled using the LightupTriggerResultOperator.
