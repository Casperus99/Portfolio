Cypress.Commands.add('createLead', (obj) => {
    cy.task('salesforceCreate', ({objectType: 'Lead', object: obj}))
})
Cypress.Commands.add('createAccount', (obj) => {
    cy.task('salesforceCreate', ({objectType: 'Account', object: obj}))
})
Cypress.Commands.add('deleteAccount', (id) => {
    cy.task('salesforceDelete', ({objectType: 'Account', id: id}))
})