FROM python
RUN pip install flask
EXPOSE 8080
CMD python3 /home/myapp/sample_app.py