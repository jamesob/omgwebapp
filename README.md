```
                                        __                      
   .-----.--------.-----.--.--.--.-----|  |--.---.-.-----.-----.
   |  _  |        |  _  |  |  |  |  -__|  _  |  _  |  _  |  _  |
   |_____|__|__|__|___  |________|_____|_____|___._|   __|   __|
                  |_____|                          |__|  |__|   
                                                                
```

## omgwebapp ➭ a minimal flask/react/webpack fun pack

![if you lived here you'd be home by now](assets/console.png)

You consider yourself a pretty decent webdev, but getting all the accoutrements going
to even start thinking about building a modern web application is an amount of work on
par with a masters degree. Your six-months out-of-date understanding of webpack is now
worse than useless. Last time you tried to get `node_modules` to work with docker's
volume mounts, you wondered about jumping off your roof instead. 

Don't spend eight weeks of your life fretting over boilerplate, just use this halfway
decent start.

### frontend 

- webpack
  - As simple a config as I could make it while being relatively fully-featured.
  - Typescript enabled
  - PostCSS configured: imports, nested CSS, and cssnano.
- bootstrap (via react-bootstrap)
  - It's simple, it works, you probably already know it.
- bootstrap table example
  - You'll need this at some point.
- yarn
  - Allows us to easily configure `node_modules` to live only in the built container.
- react-router
  - Minimal, sensible config.
- **No redux** - it's too much boilerplate, and is sort of
  [obviated by hooks](https://blog.logrocket.com/use-hooks-and-context-not-react-and-redux/). 
  I just can't be bothered anymore.
- **No test frameworks** - because really, who has the time

### backend

- python3.8
- flask
- [peewee](http://docs.peewee-orm.com/en/latest/peewee/) (ORM)
  - It's light, simple, and has all the features you want.
- [functioning asynchronous
  worker](https://github.com/jamesob/omgwebapp/blob/master/backend/changeme/worker.py):
  powered by a database queue, a sleep loop, and
  no extra dependencies. Shouldn't be too hard to add Celery if you want it.
- py.test
  - Allows [easy, Rust-style inline test functions](https://github.com/jamesob/omgwebapp/commit/cfc04617c0dffabcae0c1edde4a7cc3417204651#diff-7002a6dda08096d34c21a6f182274de1R89-R122).
  - [In-memory fixture
    database](https://github.com/jamesob/omgwebapp/commit/cfc04617c0dffabcae0c1edde4a7cc3417204651#diff-a7c56826844ee9ea851d1b5fe95e6413R7-R17) set up.
- mypy
  - TODO
- sensible logging config
  - TODO

### makefile

Sane Makefile that's essentially just aliasing for docker-compose.


### What's the example do?

![here it is](assets/screenshot.png)

The app demonstrates basic functionality in each of the pieces of tech used; it defines
database models, creates a basic API, and offers a simple interface for creating "jobs"
that ultimately get executed by an asynchronous worker process.

The web UI lets you schedule greetings. Don't get too excited now.

Obviously this should be pretty easy to change; start at
`frontend/src/components/Home.jsx` and `backend/changeme/{web,db}.py`.

### Principles

- Everything is done in docker. No dependencies are installed on host aside from 
  docker, docker-compose, and maybe make.

- I've tried to make it as straightforward as possible to swap out components. Want to
  use Django, postgres, some message queue, whatever? Shouldn't be too hard.

- Everything is served by the `server` container; a Flask webapp. This includes static
  files as well as the frontend application.

- The `webpack` container is simply responsible for compiling the frontend javascript
  and sticking it in `/build`, which is a mounted directory that is shared with the
  `server` container.

- Not particularly production ready, and doesn't want to be. 
  This isn't really geared at people running bigtime
  heavy-duty industrial strength applications; this is for people who want to get
  something lightweight and halfway decent going with enough extensibility to grow
  into production. For low-traffic web applications, it should be sufficient to slap
  this up on a single box with `docker-compose up -d` and some restart policies.

### Installation
 
I'm not using [cookiecutter](https://github.com/cookiecutter/cookiecutter) etc. because
I think it's worthwhile for you to go through and manually change the stuff that needs
changing; that way we can both pretend you have a modicum of understanding of this
boilerplate that you've wantonly downloaded from some guy on the internet.
 
Find and replace all instances of `changeme` and move the Python directory:
```sh
$ mv backend/{changeme,$YOUR_PROJECT_NAME}
$ grep -R changeme .
```

You'll need Docker and docker-compose on host, but beyond that it should be a simple
matter of running `make build up logs`. Check out the `Makefile` for more
details.

Then browse to http://localhost:7082/.

### Things you should consider doing before production

- [ ] pin and vendor all dependencies
- [ ] think about some kind of TLS solution

### Credits

Long ago, this was sort of a fork of
[flask-react-boilerplate](https://github.com/YaleDHLab/flask-react-boilerplate).
