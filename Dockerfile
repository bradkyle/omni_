FROM eboraas/openai-gym
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 5000