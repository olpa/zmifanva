all:
	@echo targets:
	@echo corpus,
	@echo en-jb, jb-en,
	@echo report-en-jb, report-jb-en,
	@echo test-en-jb, test-jb-en,

corpus: .corpus

.corpus: prepare_corpus.py $(wildcard ../docs/*.xml)
	python3 prepare_corpus.py \
	  --solr-dir ../../docs/ \
	  --seed 42 \
	  ../corpus/train/collection:60 \
	  ../corpus/tune/collection:20 \
	  ../corpus/eval/collection:20
	touch $@

en-jb: .en-jb

jb-en: .jb-en

.%: config-ems.%.ini
	mkdir -p ../tmp
	docker run -it --rm \
	  -v $(shell cd .. && pwd):/zmifanva/moses_model \
	  olpa/moses-tune \
	  /opt/moses/scripts/ems/experiment.perl \
	    -config /zmifanva/moses_model/scripts/$< \
	    -no-graph \
	    -exec
	ls -t ../tmp/tuning/tmp.*/moses.ini | head -1 | tee $@

report-%:
	$(eval report_file := $(shell cat .$* | sed 's/tuning/evaluation/' | sed 's@/moses.ini@@' | sed 's@/tmp\.@/report.@'))
	cat $(report_file)

run-model-%:
	docker run -it --rm \
	  -v $(shell cd .. && pwd):/zmifanva/moses_model \
	  olpa/moses-tune \
	  moses -f /zmifanva/moses_model/tmp/$(shell cat .$*)

dist-jb-en: ../tmp/dist/jb-en/moses.ini

dist-en-jb: ../tmp/dist/en-jb/moses.ini

../tmp/dist/%/moses.ini: .% copy_model.py
	python3 copy_model.py \
	  --from-ini $(shell cat .$*) \
	  --to-dir ../tmp/dist/$* \
	  --base-marker /tmp/ \
	  --new-path /zmifanva/moses_model/$*

run-dist-%:
	docker run -it --rm \
	  -v $(shell cd .. && pwd)/tmp/dist:/zmifanva/moses_model \
	  olpa/moses-tune \
	  moses -f /zmifanva/moses_model/$*/moses.ini

build-docker-%: dist-%
	MODELPATH=/zmifanva/moses_model/$* \
		  envsubst <Dockerfile.tpl >../tmp/dist/$*/Dockerfile
	cd ../tmp/dist/$* \
	  && docker build -t olpa/moses-zf-$* .

run-docker-%:
	docker run -it --rm olpa/moses-zf-$*

push-%:
	docker push olpa/moses-zf-$*
