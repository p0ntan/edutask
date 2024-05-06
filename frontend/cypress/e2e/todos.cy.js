describe('Interact with todos on an existing task with two todos', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let email // email of the user

  beforeEach(function () {
    // Add a user and task for test-user before each test
    cy.viewport(1366,	768)
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          email = user.email

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
              })
            }).then((res) => {
                cy.request({
                  method: 'POST',
                  form: true,
                  url: 'http://localhost:5000/todos/create',
                  body: {
                    taskid: res.body[0]._id.$oid,
                    description: 'A done todo!',
                    done: true
                  }
              }).then(() => {
                  cy.visit('http://localhost:3000')
                    .get('.inputwrapper #email')
                    .type(email)
                    .get('form')
                    .submit()
                    .get('.container-element a').click()
              })
            })
        })
      })
  })
  
  it('form should have an empty input-field and a disabled button', () => {
    cy.get('.popup form input[type=text]')
      .should('have.value', '')
    cy.get('.popup form input[type=submit]')
      .should('be.disabled')
  })

  it('should add a todo to bottom of list', () => {
    let textString = 'This is a todo for testing'

    cy.get('.popup form input[type=text]')
      .type(textString)
      .get('.popup form')
      .submit()

    cy.get('li.todo-item')
      .last()
      .should('contain.text', textString)
  })

  it('should mark the a todo as done with a strike through', () => {
    cy.get('li.todo-item').first().as('todoItem')

    cy.get('@todoItem').find('.checker').click()

    cy.get('@todoItem')
      .find('.editable')
      .should('have.css', 'text-decoration-line', 'line-through')
  })

  it('should mark the a todo as active and remove strike through', () => {
    cy.get('li.todo-item').last().as('todoItem')

    cy.get('@todoItem').find('.checker').click()

    cy.get('@todoItem')
      .find('.editable')
      .should('not.have.css', 'text-decoration-line', 'line-through')
  })

  it('should delete one todo, with one todo left in list', () => {
    cy.get('li.todo-item')
      .last()
      .find('.remover')
      .click()

    cy.get('li.todo-item')
      .its('length')
      .should('eq', 1)
  })

  afterEach(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})
