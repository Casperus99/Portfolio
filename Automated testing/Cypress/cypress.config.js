const { defineConfig } = require('cypress')
const jsforce = require('jsforce');
const username = 'nowakowski.kacperr@mindful-bear-nb7lda.com'
const password = 'Sales-Casp99XMXB0pxewtFvrIvxqNUfunpS'
const loginUrl = 'https://login.salesforce.com/'

function createObject(objectType, object, config) {
  return new Promise((resolve, reject) => {
    var conn = new jsforce.Connection({loginUrl: loginUrl})

    conn.login(username, password, err => {
      if (err) reject(err)

      conn.sobject(objectType).create(object, (err, ret) => {
        if (err || !ret.success) { return console.error(err, ret) }
        return resolve(ret)
      })
    })
  })
}

function deleteObject(objectType, id, config) {
  return new Promise((resolve, reject) => {
    var conn = new jsforce.Connection({loginUrl: loginUrl})

    conn.login(username, password, err => {
      if (err) reject(err)

      conn.sobject(objectType).destroy(id, (err, ret) => {
        if (err || !ret.success) { return console.error(err, ret) }
        return resolve(ret)
      })
    })
  })
}

module.exports = defineConfig({
  includeShadowDom: true,
  e2e: {
    setupNodeEvents(on, config) {
      on('task', {
        salesforceCreate ({objectType, object}) {
          return createObject(objectType, object, config)
        },
        salesforceDelete ({objectType, id}) {
          return deleteObject(objectType, id, config)
        },
        log(message) {
          console.log(message)
          return null
        },
        // Add new tasks created here
    }) 
    }
  }
})