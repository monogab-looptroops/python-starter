## Manifests for deployment

This folder contains all the manifests to deploy microservice to kubernetes.

It is a combination of helm and kustomize. 
  - Helm is responsible to replace values in the templates to specify configuration per single deployable unit
  - Kustomize is used to define all the units needed for a site



## Folder structure

```bash
deployment
├── base 
│   ├── example 
│   │   ├── templates  # manifest templates
│   │   │    ├── deployment.yaml 
│   │   │    │   ...
│   │   │    └── service.yaml
│   │   │   Chart.yaml   # helm chart definition 
│   │   └── values.yaml  # default values 
│   │   
│   └── chart2 ... # you can add several here
│   └── chart3 ... # if you need other deployments for the service
│       
│
└── overlays # per site configuration
    ├── clw-dev # specific site
    │   ├── argocd.yaml          # argocd application to use continues deployment
    │   ├── kustomization.yaml   # costumize deployment
    │   ├── values-example.yaml  # replacement values for example helm chart    
    │   └── values-chart2.yaml
    ...
    └── clp-prd  # another site
        ...
        └── values-chart2.yaml
```

## Usage
Check the generated yaml file:
```
kubectl kustomize overlays/clw-dev --enable-helm > output.yaml
```

## Deploy
There are two possibilities to deploy: 

1. Manually

```shell
kubectl kustomize overlays/clw-dev --enable-helm 
```

2. Argo cd
The overlays/xxx folders contain argocd
```shell
kubectl apply -f overlays/local/argocd.yaml
```