# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "flask==3.1.0",
#     "gliner==0.2.13",
#     "marimo",
#     "spacy==3.8.3",
# ]
# ///
import marimo

__generated_with = "0.10.7"
app = marimo.App(width="medium")


@app.cell
def _(labels_ui, mo, text_ui):
    markdown = mo.md(
        '''
        ## Marimo/GliNER demo

        This notebook is a bit special. It defines a UI, a CLI *and* an API in one fell swoop!

        - What is the input text?: {text}
        - What named entities would you like to detect?: {labels}
        '''
    )

    batch = mo.ui.batch(
        markdown, {"text": text_ui, "labels": labels_ui}
    )

    batch.callout()
    return batch, markdown


@app.cell
def _(batch, displacy, mo, model, spacy):
    nlp = spacy.blank("en")

    def text_to_doc(text, labels):
        labels = labels.split(",")
        entities = model.predict_entities(text, labels)
        
        doc = nlp(text)
        doc.ents = [doc.char_span(e['start'], e['end'], label=e['label']) for e in entities]
        return doc

    doc = text_to_doc(text=batch.value.get("text"), labels=batch.value.get("labels"))
    mo.Html(displacy.render(doc, style="ent"))
    return doc, nlp, text_to_doc


@app.cell
def _(app, displacy, text_to_doc):
    from flask import request

    @app.route("/api/ner", methods=["POST"])
    def infer():
        text = request.form.get("text")
        labels = request.form.get("labels")
        doc = text_to_doc(text=text, labels=labels)
        return doc.to_json()

    @app.route("/api/ner_view", methods=["POST"])
    def infer_view():
        text = request.form.get("text")
        labels = request.form.get("labels")
        doc = text_to_doc(text=text, labels=labels)
        return displacy.render(doc, style="ent")
    return infer, infer_view, request


@app.cell
def _(mo):
    text_ui = mo.ui.text_area()
    labels_ui = mo.ui.text()
    return labels_ui, text_ui


@app.cell
def _(batch, model):
    labels = batch.value.get("labels").split(",")
    entities = model.predict_entities(batch.value.get("text"), labels)
    return entities, labels


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import spacy 
    from spacy import displacy
    from spacy.tokens import Span
    return Span, displacy, spacy


@app.cell
def _():
    from gliner import GLiNER

    model = GLiNER.from_pretrained("urchade/gliner_small-v2.1")
    return GLiNER, model


@app.cell
def _(mo):
    from flask import Flask

    class MarimoApp(): 
        def __init__(self): 
            app = Flask(__name__)

            @app.route("/")
            def alive1():
                return "alive"

            @app.route("/health")
            def alive2():
                return "alive"

            @app.route("/healthz")
            def alive3():
                return "alive"

            self.flask_app = app

        def route(self, *args, **kwargs): 
            return self.flask_app.route(*args, **kwargs)

        def run(self, debug=False, port=5000, force=False):
            if mo.app_meta().mode != 'edit':
                return self.flask_app.run(debug=debug, port=port)
            if force:
                return self.flask_app.run(debug=debug, port=port)
            print("Not running app while in edit mode. Set force to True if need be.")

    app = MarimoApp()
    return Flask, MarimoApp, app


@app.cell
def _(app, mo):
    if mo.app_meta().mode != "edit":
        app.run(debug=True, port=8080)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
