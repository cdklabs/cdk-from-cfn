`export CREATE_STACK=true`

`unset CREATE_STACK`

`cargo test --test end-to-end vpc::typescript -- --nocapture`

original template.json files need to have 1 space for indentation to minimize ugliness in diffs.