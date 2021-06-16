FROM python:3.6.8 AS build
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --compile -r requirements.txt && rm -rf /root/.cache
COPY . .

# run tests
FROM build AS test
RUN pip3 install pytest pytest-cov && rm -rf /root/.cache
RUN pytest --doctest-modules \
  --junitxml=xunit-reports/xunit-result-all.xml \
  --cov

# build setting the executable
FROM build AS final
CMD [ "python", "photo_details.py" ]