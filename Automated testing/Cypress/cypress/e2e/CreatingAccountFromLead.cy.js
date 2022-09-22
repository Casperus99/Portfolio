import { Lead } from "../domain/lead"

describe('empty spec', () => {
  it('logs in', () => {
    cy
      .request({
        body: {
          display: 'page',
          hasRememberUn: 'true',
          height: '1080',
          local: '',
          locale: '',
          login: '',
          loginType: '',
          loginURL: '',
          lt: 'standard',
          oauth_callback: '',
          oauth_token: '',
          pw: 'Sales-Casp99',
          qs: '',
          serverid: '',
          startURL: '',
          un: 'nowakowski.kacperr@mindful-bear-nb7lda.com',
          useSecure: 'true',
          username: 'nowakowski.kacperr@mindful-bear-nb7lda.com',
          width: '2560',
        },
        form: true,
        method: 'POST',
        url: 'https://login.salesforce.com/',
      })

    const resizeObserverLoopErrRe = /^[^(ResizeObserver loop limit exceeded)]/
    Cypress.on('uncaught:exception', (err) => {
      /* returning false here prevents Cypress from failing the test */
      if (resizeObserverLoopErrRe.test(err.message)) {
          return false
      }
    })

    //Create new Lead
    const lead = new Lead()
    const testLastName = 'Test Name'
    const testCompanyName = 'TestCompany'
    
    lead.setLastName(testLastName)
    lead.setCompany(testCompanyName)

    cy.createLead(lead)
      .then((newLead) => {
        cy.wrap(newLead.id).as('newLeadId')
    })

    //Convert new Lead into Account
    cy.get('@newLeadId').then(newLeadId => {
      cy.visit(`https://mindful-bear-nb7lda-dev-ed.lightning.force.com/lightning/r/Lead/${newLeadId}/view`)
    })

    cy.get('[name="Convert"]').click()

    cy.wait(1000)

    cy.get('[data-aura-class="runtime_sales_leadConvertModalFooter"]').contains('Convert').click()

    cy.wait(2000)

    cy.get(`[title="${testCompanyName}"]`).first().each($item => {
      cy.wrap($item.attr('data-recordid')).as('newAccountId')
    })

    cy.get('[title="Close this window"]').first().click()

    //Check Account
    cy.get('[aria-current="false"]').contains('Accounts').click()

    cy.wait(1500)

    cy.get('[aria-label="Recently Viewed"][data-aura-class="uiVirtualDataTable"] > tbody > tr')
      .first().within(() => {
        cy.get('a').first().should(($a) => {
          expect($a).to.contain(testCompanyName)
        })
      })

    //Check Contact
    cy.get('[aria-current="false"]').contains('Contacts').click()

    cy.wait(1500)

    cy.get('[aria-label="Recently Viewed"][data-aura-class="uiVirtualDataTable"] > tbody > tr')
      .first().within(() => {
        cy.get('a').first().should(($a) => {
          expect($a).to.contain(testLastName)
        })
      })

    //Check Opportunity
    cy.get('[aria-current="false"]').contains('Opportunities').click()

    cy.wait(1500)

    cy.get('[aria-label="Recently Viewed"][data-aura-class="uiVirtualDataTable"] > tbody > tr')
      .first().within(() => {
        cy.get('a').first().should(($a) => {
          expect($a).to.contain(testCompanyName+'-')
        })
      })
    
    //Delete new Account thus new Contact and Opportunity
    cy.get('@newAccountId').then(newAccountId => {
      cy.deleteAccount(newAccountId)
    })
  })
})