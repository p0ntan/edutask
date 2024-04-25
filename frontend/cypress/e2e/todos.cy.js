describe('Interact with todos on an existing task', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  before(function () {
    // create a fabricated user from a fixture
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
      })
  })

  beforeEach(function () {
    // Go to the detalied view for a task
    cy.viewport(1920, 1080)
    cy.visit('http://localhost:3000')
    cy.get('.inputwrapper #email')
      .type(email)
    cy.get('form')
      .submit()
    cy.get('.container-element a').click()
  })

  it('should have a disabled button when input is missing', () => {
    cy.get('ul.todo-list li form input[type=submit]')
      .should('be.disabled')
  })

  // it('should add a todo to bottom of list', () => {
  //   cy.get('ul.todo-list li form input[type=text]')
  //     .type("Woop woop.")
  //   cy.get('ul.todo-list li form')
  //     .submit()
  //     .then(() => {
  //       cy.get('ul.todo-list li.todo-item')
  //         .then(() => {

  //         })
  //     })
  // })

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