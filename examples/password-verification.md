# Check password verification with a coding agent

A passing sign-in test can miss a verifier that accepts every password. Use a small local Argon2id exercise to check what succeeds and what fails. All inputs are fictional.

## Run the exercise

Use Node.js 24.7 or later in an empty folder. Download the source and read it before running it.

```sh
curl -fsSL https://hiredin60.com/argon2id-verification.mjs -o argon2id-verification.mjs
node argon2id-verification.mjs
```

```text
Correct password: true
Wrong password: false
Changed salt: false
```

The exercise derives a tag from the passphrase and a random salt. Verification derives a new tag from the proposed password and stored salt, then compares the two tags.

## Check that the test can fail

Ask your agent to run the original exercise and record its exit code. Then ask it to copy the file, change the `verify` function in the copy to return `true` for every input, and run the copy. The original should exit with code 0. The copy should fail the assertion with a nonzero exit code. Have the agent show both results and leave the original file intact.

For production sign-in, use a maintained password library and keep its algorithm, parameters and salt with the stored hash. [Node.js Argon2 API](https://nodejs.org/api/crypto.html#cryptoargon2syncalgorithm-parameters) · [OWASP password storage guidance](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#argon2id).

## Practice the interview question

Open the worked answer and download the free sample PDF. The optional Interview Quick Review Pack is $12. [Free Hired in 60 exercise](https://hiredin60.com/lessons/081/?utm_source=github&utm_medium=readme&utm_campaign=argon2id-repository-exercise#argon2id-practice).
