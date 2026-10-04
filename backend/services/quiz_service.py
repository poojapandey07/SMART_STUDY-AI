import json
from backend.models import Quiz, QuizQuestion
from backend.database.database import db

class QuizService:
    """Quiz generation and grading service."""

    SUBJECT_QUESTION_BANKS = {
        "Data Structures": [
            {
                "question": "What is the time complexity to access an element by index in an array?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                "correct_answer": "O(1)",
                "explanation": "Arrays use contiguous memory allocation, allowing constant-time O(1) random access using pointer arithmetic."
            },
            {
                "question": "Which data structure operates on a First-In, First-Out (FIFO) principle?",
                "options": ["Stack", "Queue", "Binary Tree", "Max-Heap"],
                "correct_answer": "Queue",
                "explanation": "A Queue processes elements in the order they arrive (FIFO), whereas a Stack is LIFO (Last-In, First-Out)."
            },
            {
                "question": "What is the average time complexity of searching in a Balanced Binary Search Tree?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
                "correct_answer": "O(log n)",
                "explanation": "In balanced BSTs (like AVL or Red-Black trees), the tree height is logarithmic, keeping lookups to O(log n)."
            },
            {
                "question": "Which of the following data structures is best suited for implementing undo functionality in an editor?",
                "options": ["Queue", "Stack", "Array", "Hash Table"],
                "correct_answer": "Stack",
                "explanation": "A Stack stores actions in LIFO order so the most recent edit is the first one undone."
            },
            {
                "question": "What is the worst-case time complexity of standard QuickSort?",
                "options": ["O(n log n)", "O(n)", "O(n^2)", "O(log n)"],
                "correct_answer": "O(n^2)",
                "explanation": "When pivot selection produces completely unbalanced partitions (e.g. already sorted array with first element as pivot), QuickSort degrades to O(n^2)."
            }
        ],
        "Python": [
            {
                "question": "What is the primary difference between a Python list and a tuple?",
                "options": [
                    "Lists are immutable, tuples are mutable",
                    "Lists are mutable, tuples are immutable",
                    "Tuples cannot hold multiple data types",
                    "Lists use less memory than tuples"
                ],
                "correct_answer": "Lists are mutable, tuples are immutable",
                "explanation": "Lists can be modified after creation (append, pop, slice-assign), whereas tuples cannot be altered once created."
            },
            {
                "question": "What will `bool([])` evaluate to in Python?",
                "options": ["True", "False", "None", "TypeError"],
                "correct_answer": "False",
                "explanation": "Empty sequences (lists, dictionaries, tuples, strings) evaluate to False in boolean contexts."
            },
            {
                "question": "Which Python keyword is used to create an anonymous function?",
                "options": ["def", "func", "lambda", "inline"],
                "correct_answer": "lambda",
                "explanation": "`lambda` creates small, anonymous inline functions in Python (e.g., `lambda x: x * 2`)."
            },
            {
                "question": "What is the time complexity of looking up a key in a Python dictionary on average?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
                "correct_answer": "O(1)",
                "explanation": "Python dictionaries are implemented using hash tables, giving them average O(1) lookup and insertion time."
            }
        ],
        "Database Management": [
            {
                "question": "What is the main goal of database normalization?",
                "options": [
                    "Increase query complexity",
                    "Reduce data redundancy and prevent update anomalies",
                    "Encrypt confidential tables",
                    "Convert SQL queries into NoSQL documents"
                ],
                "correct_answer": "Reduce data redundancy and prevent update anomalies",
                "explanation": "Normalization organizes fields and table relationships to minimize duplication and protect data integrity."
            },
            {
                "question": "Which normal form requires eliminating partial functional dependencies on a composite primary key?",
                "options": ["1NF", "2NF", "3NF", "BCNF"],
                "correct_answer": "2NF",
                "explanation": "Second Normal Form (2NF) mandates that all non-key attributes are fully functionally dependent on the primary key."
            },
            {
                "question": "What does the 'I' in ACID properties represent?",
                "options": ["Indexing", "Isolation", "Integrity", "Inheritance"],
                "correct_answer": "Isolation",
                "explanation": "Isolation guarantees that concurrent database transactions do not interfere with one another."
            }
        ],
        "Operating Systems": [
            {
                "question": "Which CPU scheduling algorithm gives each process a small unit of CPU time (time quantum)?",
                "options": ["First-Come, First-Served (FCFS)", "Shortest Job First (SJF)", "Round Robin (RR)", "Priority Scheduling"],
                "correct_answer": "Round Robin (RR)",
                "explanation": "Round Robin assigns a fixed time slice (quantum) to each ready process in cyclic order."
            },
            {
                "question": "What are the four necessary conditions for a deadlock to occur?",
                "options": [
                    "Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait",
                    "Paging, Segmentation, Swapping, Thrashing",
                    "Concurrency, Parallelism, Scheduling, Context Switch",
                    "Read, Write, Execute, Terminate"
                ],
                "correct_answer": "Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait",
                "explanation": "Coffman's four conditions must hold simultaneously for a deadlock state to arise in an OS."
            },
            {
                "question": "What causes thrashing in virtual memory systems?",
                "options": [
                    "Excessive CPU usage",
                    "Processes spending more time paging in/out than executing instructions",
                    "Hardware bus malfunction",
                    "Corrupted file descriptors"
                ],
                "correct_answer": "Processes spending more time paging in/out than executing instructions",
                "explanation": "When main memory is overcommitted, the OS spends nearly all CPU time swapping pages in and out of disk."
            }
        ],
        "Artificial Intelligence": [
            {
                "question": "What is the primary role of the activation function in an artificial neural network?",
                "options": [
                    "Initialize weights to zero",
                    "Introduce non-linearity so the network can learn complex patterns",
                    "Speed up database queries",
                    "Normalize input dimensions to 8 bits"
                ],
                "correct_answer": "Introduce non-linearity so the network can learn complex patterns",
                "explanation": "Without non-linear activation functions (like ReLU or Sigmoid), stacking layers would only compute linear transformations."
            },
            {
                "question": "Which algorithm calculates gradients of the loss function with respect to weights using the chain rule?",
                "options": ["Forward Propagation", "Backpropagation", "A* Search", "K-Means Clustering"],
                "correct_answer": "Backpropagation",
                "explanation": "Backpropagation computes partial derivatives layer-by-layer backwards using the calculus chain rule."
            }
        ]
    }

    @classmethod
    def generate_quiz(cls, user_id: int, subject: str, topic: str, difficulty: str, count: int) -> Quiz:
        """Create a new quiz record with questions tailored to subject and difficulty."""
        matched_bank = None
        for key, bank in cls.SUBJECT_QUESTION_BANKS.items():
            if key.lower() in subject.lower() or subject.lower() in key.lower():
                matched_bank = bank
                break
        
        if not matched_bank:
            matched_bank = cls.SUBJECT_QUESTION_BANKS["Data Structures"]

        selected_raw = matched_bank[:min(count, len(matched_bank))]
        if len(selected_raw) < count:
            while len(selected_raw) < count:
                selected_raw.append(matched_bank[len(selected_raw) % len(matched_bank)])

        quiz = Quiz(
            user_id=user_id,
            subject=subject,
            topic=topic or "General",
            difficulty=difficulty or "medium",
            total_questions=len(selected_raw),
            score=0,
            percentage=0.0,
            completed=False
        )
        db.session.add(quiz)
        db.session.flush()

        for q_data in selected_raw:
            question_obj = QuizQuestion(
                quiz_id=quiz.id,
                question=q_data["question"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                explanation=q_data.get("explanation", "")
            )
            db.session.add(question_obj)

        db.session.commit()
        return quiz

    @classmethod
    def grade_quiz(cls, quiz: Quiz, answers: dict) -> dict:
        """Grade submitted answers and calculate backend score."""
        answer_map = {}
        if isinstance(answers, list):
            for item in answers:
                answer_map[int(item.get("question_id", 0))] = str(item.get("answer", "")).strip()
        elif isinstance(answers, dict):
            for k, v in answers.items():
                try:
                    answer_map[int(k)] = str(v).strip()
                except ValueError:
                    pass

        correct_count = 0
        total = len(quiz.questions)

        for q in quiz.questions:
            user_ans = answer_map.get(q.id, "")
            q.user_answer = user_ans
            q.is_correct = (user_ans.lower() == q.correct_answer.lower())
            if q.is_correct:
                correct_count += 1

        quiz.score = correct_count
        quiz.total_questions = total
        quiz.percentage = round((correct_count / total) * 100, 1) if total > 0 else 0.0
        quiz.completed = True

        db.session.commit()

        return {
            "quiz_id": quiz.id,
            "score": quiz.score,
            "total_questions": quiz.total_questions,
            "percentage": quiz.percentage,
            "passed": quiz.percentage >= 60.0,
            "questions": [q.to_dict() for q in quiz.questions]
        }
