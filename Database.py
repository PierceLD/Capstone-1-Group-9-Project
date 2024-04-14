import sqlite3

def getAllSetNames():
    """ Returns all set names as list of strings.
    """
    names = []

    try:
        conn = sqlite3.connect('study_sets.db')
        cursor = conn.cursor()

        query = """
            SELECT DISTINCT Name FROM Sets
        """
        cursor.execute(query)
        result = cursor.fetchall()
        
        names = [row[0] for row in result]
    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()
    
    return names

def getSetQuestions(name):
    """ Returns all questions of a specified set as a list of dictionaries.
        Returns empty list if set doesn't exist.
    """
    questions = []
    if name in getAllSetNames():
        try:
            conn = sqlite3.connect('study_sets.db')
            cursor = conn.cursor()

            query = """
                SELECT Question, A, B, C, D, Correct_Answer FROM Sets WHERE Name = ?
            """
            cursor.execute(query, (name,))
            result = cursor.fetchall()
            
            for row in result:
                questions.append({
                        "question": row[0],
                        "A": row[1],
                        "B": row[2],
                        "C": row[3],
                        "D": row[4],
                        "answer": row[5]
                    }
                )

        except sqlite3.Error as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()
    else:
        print("Set does not exist.")

    return questions

def getAllSets():
    """ Returns dictionary with keys being set names, and values being a list of that set's questions.
    """
    sets = {}
    for set_name in getAllSetNames():
        questions = getSetQuestions(set_name)
        sets[set_name] = questions

    return sets

def insertQuestion(set_name: str, question: dict):
    """ Inserts a new question and its values into specified study set."""
    try:
        conn = sqlite3.connect('study_sets.db')
        cursor = conn.cursor()

        query = """
            INSERT INTO Sets(Name, Question, A, B, C, D, Correct_Answer) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        options = question["options"] # list of options
        correct_option = question["correct_option"][0]
        if correct_option == 0:
            correct_option = "A"
        elif correct_option == 1:
            correct_option = "B"
        elif correct_option == 2:
            correct_option = "C"
        elif correct_option == 3:
            correct_option = "D"
        cursor.execute(query, (set_name, question["text"], options[0], options[1], options[2], options[3], correct_option,))

        conn.commit()
    except sqlite3.Error as e:
        print("Error:", e)
        print("Question already exists.")
    finally:
        cursor.close()
        conn.close()

def removeQuestion(set_name: str, question: str):
    """ Removes a specified question from specified study set.
    """
    try:
        conn = sqlite3.connect('study_sets.db')
        cursor = conn.cursor()

        query = """
            DELETE FROM Sets WHERE Name = ? AND Question = ?
        """
        cursor.execute(query, (set_name, question,))

        conn.commit()
    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

def insertStudySet(set_name: str, questions: list[dict]):
    """ Inserts a new study set and all its questions.\
        Can be used when inserting study sets from JSON files.
    """
    if set_name not in getAllSetNames():
        try:
            conn = sqlite3.connect('study_sets.db')
            cursor = conn.cursor()

            # insert data
            for q in questions:
                query = """
                    INSERT INTO Sets(Name, Question, A, B, C, D, "Correct_Answer") VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                options = q["options"] # list of options
                correct_option = q["correct_option"][0]
                if correct_option == 0:
                    correct_option = "A"
                elif correct_option == 1:
                    correct_option = "B"
                elif correct_option == 2:
                    correct_option = "C"
                elif correct_option == 3:
                    correct_option = "D"
                cursor.execute(query, (set_name, q["text"], options[0], options[1], options[2], options[3], correct_option,))
                #cursor.execute(query, (set_name, q["question"], q["A"], q["B"], q["C"], q["D"], q["answer"],))

            conn.commit()
        except sqlite3.Error as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()
    else:
        print("Study set of that name already exists. Pick a new set name.")

def removeStudySet(name):
    """ Removes all tuples from a specified study set.
    """
    try:
        conn = sqlite3.connect('study_sets.db')
        cursor = conn.cursor()

        query = """
            DELETE FROM Sets WHERE Name = ?
        """
        cursor.execute(query, (name,))

        conn.commit()
    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

def updateQuestion(set_name: str, old_question: str, new_question: str, A: str, B: str, C: str, D: str, correct_answer: str):
    """ Updates a specified question from a specified set.
    """
    try:
        conn = sqlite3.connect('study_sets.db')
        cursor = conn.cursor()

        query = """
            UPDATE Sets
            SET Question = ?, A = ?, B = ?, C = ?, D = ?, Correct_Answer = ?
            WHERE Name = ? AND Question = ?
        """
        cursor.execute(query, (new_question, A, B, C, D, correct_answer, set_name, old_question,))

        conn.commit()
    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()