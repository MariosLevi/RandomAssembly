from flask import Flask, render_template, request, session
import random

app = Flask(__name__)

# Set a secret key for the session
app.secret_key = "my_secret_key"

def generate_phrases(words):
  if not words:
    return []

  # List of possible phrases
  phrases = ["attached to", "beside", "around", "over", "in", "on", "under", "containing"]

  # Shuffle the list of words
  random.shuffle(words)

  # Generate a list of random phrases
  result = []
  for i in range(len(words) - 1):
    phrase = random.choice(phrases)
    result.append(words[i] + " " + phrase + " " + words[i + 1])
    phrases.remove(phrase)

  # Add a random phrase for the last word, if possible
  if phrases:
    result.append(words[-1] + " " + random.choice(phrases))

  return result

@app.route("/", methods=["GET", "POST"])
def home():
  # Initialize the result
  result = []

  if request.method == "POST":
    if "regenerate" in request.form:
      # Get the list of words from the session
      words = session["words"]

      # Regenerate the list of phrases
      result = generate_phrases(words)
    else:
      # Get the list of words from the form
      words = request.form["words"].split(",")

      # Store the list of words in the session
      session["words"] = words

      # Generate the list of phrases
      result = generate_phrases(words)

  return render_template("index.html", result=result)

if __name__ == "__main__":
  app.run()
