FROM mongo:3.4 

MAINTAINER  <xian1i> daitaomail@gmail.com 


ENV MONGODB_ADMIN_USER admin
ENV MONGODB_ADMIN_PASS admin
ENV MONGODB_APPLICATION_DATABASE assets
ENV MONGODB_APPLICATION_USER assets
ENV MONGODB_APPLICATION_PASS thisispw$$
ENV MONGODB_LOGPATH /logs/mongodb.log
ENV AUTH yes


RUN mkdir -p /mongodb/scripts/
RUN mkdir -p /logs

VOLUME /logs

ENV SCRIPT_ROOT /mongodb/scripts

COPY ./scripts/run.sh $SCRIPT_ROOT/run.sh
RUN chmod +x $SCRIPT_ROOT/run.sh

COPY ./scripts/set_password.sh $SCRIPT_ROOT/set_password.sh
RUN chmod +x $SCRIPT_ROOT/set_password.sh

CMD ["/mongodb/scripts/run.sh"]