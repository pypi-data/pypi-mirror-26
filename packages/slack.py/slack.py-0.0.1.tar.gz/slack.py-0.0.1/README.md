# Slack CMD

A command line tool to interface slack.

## Install
(TODO)

## Usage

### Basic Usage

All the subcommands require a Slack access token to work. You can pass the token either as a parameter:

```bash
$ python main.py -a <AUTH-TOKEN> auth_test
```

or as an environment variable:

```bash
$ SLACK_API_TOKEN=<AUTH-TOKEN> python main.py auth_test
```

Authentication in Slack is based on OAuth and might be complicated to set it up. To get started, you can generate a personal token from this page: [https://api.slack.com/custom-integrations/legacy-tokens](https://api.slack.com/custom-integrations/legacy-tokens)

### Channels

This commands allows you to interact with Slack channels (listing, archiving or deleting them). All these subcommands accept filters like `--starts-with` or `--contains`. Deleting and Archiving allow `--dry-run` mode to simulate the behavior without making real changes. **Be aware of Slack API Rates. See section below**

See examples below.

#### Listing Channels

![image](https://user-images.githubusercontent.com/872296/31579597-cf395b06-b10f-11e7-8fd2-fc9681396dff.png)


List channels' ids, names, archived status:

```bash
$ python main.py -a <AUTH-TOKEN> channels
```

You can filter by `--starts-with`:

```bash
$ python main.py -a <AUTH-TOKEN> channels --starts-with 'z-visitor'
```

And `--contains`:

```bash
$ python main.py -a <AUTH-TOKEN> channels --contains 'visitor'
```

#### Archiving and Deleting Channels
**_(Warning: Once a channel is deleted there's no way to restore it. Use it at your own risk)_**

Use your usual `channels` filters and pass the `--archive` or `--delete` flags to either archive or delete the matching channels. **Try with the `--dry-run` flag before performing the real action to see which channels would be deleted.

```bash
$ python main.py -a <AUTH-TOKEN> channels --starts-with 'z-visitor' --delete --dry-run --sleep 0
```

The `--sleep` parameter is required for `--archive` and `--delete` due to Slack API Rates. See below.

Finally, a **real** `--delete` command looks like:

```bash
$ python main.py -a <AUTH-TOKEN> channels --starts-with 'z-visitor' --delete
```

## Slack API Rates

Some commands like `--delete` channels can't be issued too frequently because the Slack API fails. That's why most commands have a `--sleep` parameter that will wait a given number of milliseconds before issuing new requests. You can try decreasing it by just passing `--sleep` to your commands. I couldn't find any official documentation for the correct time limits of some methods. I tried out and for example, deleting channels requires at least 10 seconds before every request.
