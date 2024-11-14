from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.qa_service import QAService
from app.models.question import QAResponse, QuestionAnswer
import tempfile
import os

router = APIRouter()
qa_service = QAService()

@router.post("/qa", response_model=QAResponse)
async def question_answering(
    document: UploadFile = File(...),
    questions: UploadFile = File(...)
):
    """Process a document and answer questions about it."""
    try:
        # Save uploaded files temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=document.filename[-4:]) as tmp_doc:
            tmp_doc.write(await document.read())
            doc_path = tmp_doc.name

        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp_questions:
            tmp_questions.write(await questions.read())
            questions_path = tmp_questions.name

        # Process document
        file_type = document.filename.split('.')[-1].lower()
        if file_type not in ['pdf', 'json']:
            raise HTTPException(status_code=400, detail="Unsupported document format")

        # Process document and create QA chain
        vectorstore = qa_service.process_document(doc_path, file_type)
        qa_chain = qa_service.create_qa_chain(vectorstore)

        # Load and process questions
        questions_list = qa_service.load_questions(questions_path)

        # Generate answers
        results = []
        for question in questions_list:
            response = qa_chain({"query": question})
            results.append(QuestionAnswer(
                question=question,
                answer=response['result']
            ))

        # Clean up temporary files
        os.unlink(doc_path)
        os.unlink(questions_path)

        return QAResponse(results=results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))