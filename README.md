### YATR

YATR ( Yet Another Terraform Registry ) is a [Flask](https://github.com/pallets/flask) app served with [gunicorn](https://github.com/benoitc/gunicorn) inside a container.

YATR is different from other simple registries in that it automagically serves module archives by compressing module sources on the fly. Just pass in a modules path variable.

This is useful in cases where you want to use local module sources with version contstraints.


## Usage

Start by cloning:

```
git clone git@github.com:testmad/yatr.git
cd yatr
```

Build the container image:

```
podman build -t yatr .
```

Assuming the following folder structure exists in your `$HOME` folder:
```
dev
└── terraform
    └── modules
           └── fake
               └── test
                    ├── my_random
                    │   ├── 0.1.0
                    │   │   └── main.tf
                    │   └── 0.2.0
                    │       └── main.tf
                    └── my_string
                        ├── 0.1.0
                        │   ├── files
                        │   │   └── ansible.yaml
                        │   └── main.tf
                        └── 0.2.0
                            └── main.tf

```
>The above structure for a module would be as below using hashicorps naming conventions:
```
<system>\<namespace>\<name>\VERSION
```

Start a container using the YATR image passing in a mount to your modules:

```
podman run -dt --rm --network host \
-v $HOME/dev/terraform/modules:/terraform/modules:z \
yatr:latest
```

Verify by opening [http://localhost:8787](http://localhost:8787) in your browser.

You'll need to use a proxy to handle terraforms HTTPS requirement. You can use a service like [localtunnel](https://github.com/localtunnel/localtunnel) in a pinch.

```
npm install -g localtunnel
lt -p 8787 -s $USER --local-host "127.0.0.1" -o --print-requests
```

Usage in your `main.tf`:
```
module "string" {
  source = "testmad.loca.lt/test/my_string/fake"
  version = "0.2.0"
}
```


## Development

Start by cloning:

```
git clone git@github.com:testmad/yatr.git
cd yatr
```

Create and start virutal env:

```
python -m venv .venv
source .venv/bin/activate
```

Update pip:

```
pip install --upgrade pip
```

Install dependecies:

```
pip install -r requirements.txt
```

Create `.env` file:

```
cp .env.example .env
```

Start gunicorn:

```
gunicorn -w 4 --reload -b 127.0.0.1:8787 "app.app:app"
```

You'll need to use a proxy to handle terraforms HTTPS requirement. You can use a service like [localtunnel](https://github.com/localtunnel/localtunnel) in a pinch.

```
npm install -g localtunnel
lt -p 8787 -s $USER --local-host "127.0.0.1" -o --print-requests
```
