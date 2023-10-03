import urllib.request
import json
import os
import ssl

import streamlit as st


ENDPOINT_KEY = os.environ["ENDPOINT_KEY"]


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script


st.set_page_config(page_title='Tim Sbott', page_icon="✅", layout="wide")

st.title("Tim Sbott - Your (almost) perfect HR assistant")
st.image('./res/tim_transparent.png')

col1, col2 = st.columns(2)
with col1:
    query = st.text_input('Question:')
with col2:
    st.text(' ')
    st.text(' ')
    asked_tim = st.button('Ask Tim!', key='tim')
if asked_tim:
    if query:
        with col1:
            with st.spinner('Thinking about it...'):
                data = {'text': str(query)}

                body = str.encode(json.dumps(data))
                url = 'https://fletchers-ai-ws-uksouth-xxgmo.uksouth.inference.ml.azure.com/score'
                # Replace this with the primary/secondary key or AMLToken for the endpoint
                api_key = ENDPOINT_KEY
                if not api_key:
                    raise Exception("A key should be provided to invoke the endpoint")

                # The azureml-model-deployment header will force the request to go to a specific deployment.
                # Remove this header to have the request observe the endpoint traffic rules
                headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

                req = urllib.request.Request(url, body, headers)

                response = urllib.request.urlopen(req)

                result = response.read().decode("utf-8", 'ignore')[2:-2].replace('\\n', '\n')

            st.write(result)

st.title('_Query examples_')
st.text('• How many holiday days can roll over to the next year?')
st.text('• How can I contact HR?')
st.text('• Where can I access my payslips?')
st.text('• What is medicash?')
st.text('• What is Fletcher\'s stance on diversity?')
