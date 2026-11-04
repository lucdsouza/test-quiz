import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_raises_exception_for_invalid_choices():
    with pytest.raises(Exception):
        Choice(id=1, text='')
        
    with pytest.raises(Exception):
        Choice(id=1, text='a' * 101)

def test_add_multiple_choices_auto_increment_ids():
    question = Question(title='Quiz')
    c1 = question.add_choice('Choice 1')
    c2 = question.add_choice('Choice 2')

    assert c1.id == 1
    assert c2.id == 2

def test_remove_choice_by_id_successfully():
    question = Question(title='Quiz')
    c1 = question.add_choice('Choice 1')

    question.remove_choice_by_id(c1.id)

    assert len(question.choices) == 0

def test_remove_nonexistent_choice_raises_exception():
    question = Question(title='Quiz')

    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

def test_remove_all_choices_successfully():
    question = Question(title='Quiz')
    question.add_choice('Choice 1')
    question.add_choice('Choice 2')

    question.remove_all_choices()

    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='Quiz')
    c1 = question.add_choice('Choice 1', is_correct=False)
    c2 = question.add_choice('Choice 2', is_correct=False)
    
    question.set_correct_choices([c2.id])

    assert not c1.is_correct
    assert c2.is_correct

def test_set_correct_choices_with_invalid_id_raises_exception():
    question = Question(title='Quiz')
    question.add_choice('Choice 1')
    
    with pytest.raises(Exception):
        question.set_correct_choices([999])

def test_correct_selected_choice_id_is_returned():
    question = Question(title='Quiz', max_selections=2)
    c1 = question.add_choice('Choice 1', is_correct=False)
    c2 = question.add_choice('Choice 2', is_correct=True)
    c3 = question.add_choice('Choice 3', is_correct=True)
    
    correct_selected = question.correct_selected_choices([c1.id, c2.id])

    assert correct_selected == [c2.id]

def test_selected_choices_exceeds_max_selections_raises_exception():
    question = Question(title='Quiz', max_selections=1)
    c1 = question.add_choice('Choice 1')
    c2 = question.add_choice('Choice 2')
    
    with pytest.raises(Exception):
        question.correct_selected_choices([c1.id, c2.id])

def test_question_points_out_of_bounds_raises_exception():
    with pytest.raises(Exception):
        Question(title='Quiz', points=0)

    with pytest.raises(Exception):
        Question(title='Quiz', points=101)

@pytest.fixture
def common_question():
    question = Question(title='Qual a capital de Minas Gerais?', points=10, max_selections=1)
    question.add_choice('São Paulo', is_correct=False)
    question.add_choice('Belo Horizonte', is_correct=True)
    question.add_choice('Buenos Aires', is_correct=False)

    return question

def test_question_correction_with_fixture(common_question):
    correct_ids = common_question.correct_selected_choices([2])

    assert correct_ids == [2]


def test_question_incorrect_selection_with_fixture(common_question):
    correct_ids = common_question.correct_selected_choices([1])

    assert correct_ids == []

