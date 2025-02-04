# Context-dependent reinforcement-learning task

The repository replicates the task described in Gueguen et al. (2024) in PsychoPy. The task is also used and descsribed in Bavard et al. (2021; Exp. 7).

## Todos

- [ ] Implement left/right shuffle (currently called `stim1pos`)
- [ ] Implement random assignment of icons to choice options
- [ ] Implement explicit phase 
- [ ] Fix instruction slideshow
- [ ] Ensure all data is recorded (ideally, just include all condition data)
- [ ] Prepare serial port triggers (via `exp_info`?)
- [ ] Move timing variables into `exp_info` (currently hardcoded in `trial.run()`)
- [ ] Make trials look nicer

## Details

### Stimulus images

Stimulus images are made with the [Identicon generator](http://identicon.net/).

## References

- Bavard, S., Rustichini, A., & Palminteri, S. (2021). Two sides of the same coin: Beneficial and detrimental consequences of range adaptation in human reinforcement learning. Science Advances, 7(14), eabe0340. https://doi.org/10.1126/sciadv.abe0340
- Gueguen, M. C. M., Anlló, H., Bonagura, D., Kong, J., Hafezi, S., Palminteri, S., & Konova, A. B. (2024). Recent Opioid Use Impedes Range Adaptation in Reinforcement Learning in Human Addiction. Biological Psychiatry, 95(10), 974–984. https://doi.org/10.1016/j.biopsych.2023.12.005
