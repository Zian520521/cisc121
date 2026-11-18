# Verification report — 18 November 2026

This report records observed results from the deployed application and its Python test suite.

## Manual browser verification

| Test | Input or action | Observed result | Status |
|---|---|---|---|
| Default ranking | Union St 45, Library 20, Residence 70, Gym 35, West Campus 55 | Residence 70, West Campus 55, Union St 45, Gym 35, Library 20 | Pass |
| Step visualization | Start, Merge (step 9/17), Finished (step 17/17) | Bar chart, step labels, slider, and navigation responded | Pass |
| Stable tie handling | Union St 50, Library 50, Residence 80, Gym 20 | Residence 80, Union St 50, Library 50, Gym 20; tie order preserved | Pass |
| Single stop | Library 50 | Library ranked #1 | Pass |
| Invalid input | Library,abc | User-facing error: “Line 1: crowd count must be a whole nonnegative number.” | Pass |

The manual tests were documented by six genuine screenshots captured from the hosted Hugging Face page (which embeds the Render-hosted Gradio app). The screenshots were collected into a separate evidence archive; they have **not** yet been uploaded into this GitHub repository.

## Automated tests

The accompanying `test_app.py` contains nine unit tests for ordinary sorting, a single record, stability, zero and maximum counts, reverse order, invalid values, invalid names, record limits, and result text. The tests were rerun locally on 18 November 2026: **9 passed, 0 failed**.

## Hosting and limitations

- Python/Gradio runs on Render: https://cisc121-shuttle-merge-sort.onrender.com
- Hugging Face link: https://huggingface.co/spaces/Frank520521/cisc121-shuttle-merge-sort
- The Hugging Face Space is a **Static Space with an iframe**. It is not a native Python Gradio Space. An instructor who specifically requires Python execution on Hugging Face may not accept this hosting arrangement.
- The Render free tier may sleep while idle.
- The chart-label contrast was subsequently adjusted in the Python source; screenshots were captured before the final contrast fix was deployed.
- Invalid input intentionally displays a Gradio error while preserving the previous successful output. It does not mean the server crashed.
