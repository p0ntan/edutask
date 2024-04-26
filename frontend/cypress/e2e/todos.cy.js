describe('Interact with todos on an existing task', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user
  let taskId // taskId

  before(function () {
    // Create a test-user
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
        })
      })
  })

  beforeEach(function () {
    // Add task for test-user before each test
    // Contains one todo "Hold my beer and watch this"
    cy.fixture('test-task.json')
    .then((task) => {
      cy.request({
        method: 'POST',
        form: true,
        url: 'http://localhost:5000/tasks/create',
        body: {
          userid: uid,
          ...task
        }
      }).then((response) => {
        taskId = response.body[0]._id.$oid
      })
    })

    // Go to the detalied view for a task
    cy.visit('http://localhost:3000')
      .get('.inputwrapper #email')
      .type(email)
      .get('form')
      .submit()
      .get('.container-element a').click()
  })

  it('form should have an empty input-field and a disabled button', () => {
    cy.get('.popup form input[type=text]')
      .should('have.value', '')
    cy.get('.popup form input[type=submit]')
      .should('be.disabled')
  })

  it('should add a todo to bottom of list', () => {
    let textString = "This is a todo for testing"

    cy.get('.popup form input[type=text]')
      .type(textString)
      .get('.popup form')
      .submit()

    cy.get('li.todo-item')
      .last()
      .should('contain.text', textString)
  })

  it('should mark the a todo as done with a strike through', () => {
    cy.get('li.todo-item')
      .first()
      .find('.checker')
      .click()

    cy.wait(100)

    cy.get('li.todo-item')
      .first()
      .find('.editable')
      .invoke('css', 'text-decoration')
      .should('include', 'line-through')
  })

  it('should mark the a todo as active and remove strike through', () => {
    cy.get('li.todo-item')
      .first()
      .find('.checker')
      .click()

    cy.wait(100)

    cy.get('li.todo-item')
      .first()
      .find('.checker')
      .click()

    cy.wait(100)

    cy.get('li.todo-item')
      .first()
      .find('.editable')
      .invoke('css', 'text-decoration')
      .should('not.include', 'line-through')
  })

  it('should delete the todo', () => {
    cy.get('li.todo-item')
      .last()
      .find('.remover')
      .click()

    cy.wait(100)

    cy.get('li.todo-item')
      .should('not.exist')
  })

  afterEach(function () {
    // Remove task after each testcase
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/tasks/byid/${taskId}`
    }).then((response) => {
      cy.log(response.body)
    })
  })

  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})
