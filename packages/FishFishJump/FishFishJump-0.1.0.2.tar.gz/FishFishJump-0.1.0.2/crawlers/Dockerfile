FROM python:3.6-onbuild

MAINTAINER SylvanasSun sylvanas.sun@gmail.com

RUN pip install -r requirements.txt

RUN cd scrapyd
RUN python setup.py install
RUN cd ..
RUN cd scrapyd-client
RUN python setup.py install
RUN cd ..

CMD ["scrapyd"]