# Build a moses model

[Moses](https://www.statmt.org/moses/) is a statistical machine translation system. We use [Experiment Management System](http://www.statmt.org/moses/?n=FactoredTraining.EMS) (EMS) to tune the model.

### Build the corpus

```
make corpus
```

- load the corpus from the directory [../../docs/](../../docs/)
- split on 60% train, 20% tuning and 20% validation
- store the moses corpus in `../tmp/`

### Train

```
make en-jb
make jb-en
```

Each direction takes a few hours.

Input: [./config-ems.en-jb.ini](./config-ems.en-jb.ini), [./config-ems.jb-en.ini](./config-ems.jb-en.ini).

Output: many files. The path to the generated moses config is stored in the files `.en-jb` and `.jb-en`. The expected value is something like `../tmp/tuning/tmp.1/moses.ini`.

### Report

As of April 2022:

```
$ make report-en-jb
zmifanva: 87.45 (1.000) BLEU
$ make report-jb-en
zmifanva: 90.01 (0.993) BLEU
```

The original model from `mhagiwara` with some MERT tuning gave:

```
BLEU = 24.17, 60.6/32.3/17.4/10.4 (BP=0.989, ratio=0.989, hyp_len=465, ref_len=470)
BLEU = 28.06, 61.2/35.9/22.9/15.0 (BP=0.951, ratio=0.952, hyp_len=420, ref_len=441)
```

No idea what does these numbers mean.

### Run trained model

```
$ make run-model-en-jb
$ make run-model-jb-en
```

### Prepare the model for distribution

```
$ make dist-en-jb
$ make dist-jb-en
```

Copy model to `../tmp/dist/`, tune the paths inside the ini-files.

### Run the distribution-model

```
$ make run-dist-en-jb
$ make run-dist-jb-en
```

### Build docker images

```
$ make build-docker-en-jb
$ make build-docker-jb-en
```

### Run the containerized models

```
$ make run-docker-en-jb
$ make run-docker-jb-en
```
