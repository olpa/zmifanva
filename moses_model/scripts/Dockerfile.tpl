FROM ubuntu:20.04
COPY --from=olpa/moses-tune /opt/moses/bin/moses /opt/moses/bin/moses

COPY . $MODELPATH/

CMD ["/opt/moses/bin/moses", "-f", "$MODELPATH/moses.ini"]
