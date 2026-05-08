# Cathedral SN39 Validator Handoff

This is the validator handoff for Cathedral on Bittensor SN39.

Cathedral is in its compute-validation phase today. A validator runs the Cathedral validator, checks miner machines, records verification evidence, scores the available compute, and sets weights on SN39 from a permitted validator hotkey.

The point of this handoff is to let SN39 validators run the validator themselves, or child-hotkey the Cathedral operator so the experiment can run end to end while the validator keeps control.

## What the validator does now

- Reads the SN39 metagraph on Finney.
- Discovers registered Cathedral miners.
- Contacts miner gRPC endpoints.
- Opens SSH sessions to declared machines.
- Verifies machine reachability, GPU or CPU profile, Docker capability, storage, and network signals.
- Writes local verification evidence.
- Attempts `set_weights` from the configured validator hotkey.

Today this is compute validation. The next step is demand-led scoring from Polaris jobs, where miners submit deployable improvements that make real agent jobs cheaper, faster, or more reliable.

## Who should run this

Run this if you are an SN39 validator with permit, or if you operate infrastructure for one.

If you do not want to run infrastructure yet, child-hotkeying the Cathedral operator is also useful for the experiment.

Current Cathedral operator hotkey:

```text
5DnvAgAVykQFmgTSwLXTHpzfmi6W32VtV8L1D9yxSmtThWPb
```

## Requirements

- Linux server with stable network.
- Rust toolchain for the source build path.
- Bittensor CLI and a hotkey registered on SN39.
- A hotkey with validator permit for production weight setting.
- Inbound TCP `8080` for the validator API and advertised endpoint.
- Inbound TCP `50052` for miner bid registration.
- Optional private TCP `9090` for Prometheus metrics.
- Outbound SSH to miner machines.

Keep the coldkey off the server. The validator server only needs the hotkey that signs validation and weight-setting operations.

## Quick start from source

```bash
git clone https://github.com/bigailabs/cathedral.git
cd cathedral

cp config/cathedral-validator.toml.example config/validator.toml
$EDITOR config/validator.toml
```

Set these fields before running:

```toml
[server]
advertised_host = "YOUR_PUBLIC_IP"

[bittensor]
wallet_name = "YOUR_WALLET_NAME"
hotkey_name = "YOUR_HOTKEY_NAME"
network = "finney"
netuid = 39
external_ip = "YOUR_PUBLIC_IP"
```

Confirm your wallet can see SN39:

```bash
btcli wallet overview --all --netuids 39 --network finney
```

Build and run:

```bash
cargo build --release -p basilica-validator --bin cathedral-validator
RUST_LOG=info,cathedral_validator=debug \
  ./target/release/cathedral-validator --config config/validator.toml start
```

## Health checks

In another shell:

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/miners
curl http://127.0.0.1:9090/metrics
```

In logs, look for:

```text
Selected ALL
validation cycle
Updating scores
```

A permitted validator should see weight-setting attempts land once miners are verified and scores are available.

## Firewall

Example using `ufw`:

```bash
sudo ufw allow 8080/tcp
sudo ufw allow 50052/tcp
sudo ufw allow from YOUR_MONITORING_IP to any port 9090 proto tcp
```

Do not expose SSH broadly if you can avoid it. Restrict SSH to your own admin IPs.

## Current operator reference

The Cathedral operator is running this source-build path today on a Verda CPU node:

- validator API health returns `200`
- validator API reports `15` active miners
- Prometheus reports `basilica_validator_discovered_miners_total 15`
- public Cathedral log stream returns `connected: true` and `error: null`

This is the same path validators should run from their own permitted hotkey.

## Validator packet to share

- Repo: <https://github.com/bigailabs/cathedral>
- Validator guide: <https://github.com/bigailabs/cathedral/blob/main/docs/validator.md>
- Example config: <https://github.com/bigailabs/cathedral/blob/main/config/cathedral-validator.toml.example>
- Public site: <https://cathedral.computer>
- Policy: <https://github.com/bigailabs/cathedral/blob/main/docs/policy.md>

## Current mechanism

Cathedral should not reward random workflows or idle inventory. The current validator checks whether submitted compute is real and reachable. The launch direction is:

1. Polaris runs real agent jobs.
2. Miners submit deployable improvements to those jobs.
3. Cathedral validators score evidence: deployability, hidden evals, maintenance burden, and downstream Polaris usage.
4. Rewards flow to assets that make jobs cheaper, faster, or more reliable.

This creates a demand-led flywheel for Bittensor infrastructure instead of another supply-only subnet.

## Support

Open an issue here if you are running a validator and hit setup trouble:

<https://github.com/bigailabs/cathedral/issues>

Mention:

- validator hotkey
- server OS
- public IP or advertised host
- last 100 lines of validator logs
- whether the hotkey has validator permit

## Origin

Cathedral carries forward an open-source compute validator codebase and is moving the public surface, docs, and launch mechanism to Cathedral on SN39. Historical origin details live in the repository README and credits.
