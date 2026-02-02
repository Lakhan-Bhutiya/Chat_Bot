# Neuro-Chat: A Vector-Space Intelligence

> *"This is not a model. This is pure mathematics."*

## The Axiom
Forget neural hallucinations and black-box magic. **Neuro-Chat** is built on the deterministic elegance of **Linear Algebra**. It doesn't "think"; it calculates. It maps human language into a high-dimensional vector space and finds the nearest truth using the angle between thoughts.

## The Equation
The core intelligence of this system relies on **Cosine Similarity** within a **TF-IDF (Term Frequency-Inverse Document Frequency)** vector space.

Given a user query vector $\mathbf{A}$ and a knowledge base vector $\mathbf{B}$, the relevance score is defined as:

$$
\text{similarity} = \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}
$$

Where:
-   $\mathbf{A} \cdot \mathbf{B}$ is the dot product of the vectors.
-   $\|\mathbf{A}\|$ and $\|\mathbf{B}\|$ are the Euclidean magnitudes.

If $\cos(\theta) \ge 0.60$, the system accepts the hypothesis and returns the answer.
If $0.40 \le \cos(\theta) < 0.60$, the system offers probabilistic suggestions.
Else, it rejects the input as noise.

## The Matrix (Tech Stack)
-   **Django 5.2**: The web framework serving the interface.
-   **Scikit-Learn**: For `TfidfVectorizer` and `cosine_similarity`.
-   **NLTK**: For `WordNetLemmatizer` and stopword removal (noise reduction).
-   **Pandas**: For data frame manipulation.
-   **Django Jazzmin**: For a futuristic Admin UI.

## The Protocol (Installation)

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Lakhan-Bhutiya/Chat_Bot.git
    cd Chat_Bot
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize Database**
    ```bash
    python manage.py migrate
    ```

4.  **Load Knowledge Base (The Vector Space)**
    This script loads the `Question&ans.csv` into the database and vectorizes it.
    ```bash
    python setup_data.py
    ```

5.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

## The Operator (Administration)
Access the neural control panel at `/admin`.
-   **Username**: `admin`
-   **Password**: `admin` (Change this immediately in production)

Here you can inject new data vectors (CSV) or manually adjust specific dimensions (questions). The bot recalculates its vector space upon every save.

---

