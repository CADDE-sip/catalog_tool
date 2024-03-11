import { useStore } from '../stores/store'

const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '/', component: () => import('pages/Toppage.vue') },
      {
        path: '/logout',
        beforeEnter(to, from, next) { window.location = to.query.logoutUrl }
      },
      { 
        path: '/load',
        component: () => import('pages/LoginLoad.vue'),
        beforeEnter(to, from, next) {
          var store = useStore()
          store.updateAuthInfo({
            keycloakState: to.query.state,
            keycloakCode: to.query.code
          })
          next()
        }
      },
      { 
        path: '/keycloak',
        name: 'keycloak',
        beforeEnter(to, from, next) { window.location = to.query.keycloakUrl }
      },
      { path: '/login', component: () => import('pages/Login.vue') },
      { path: '/menuSelect', component: () => import('pages/MenuSelect.vue'), meta: { login_required: true } },      
      { path: '/register', component: () => import('pages/Dataset.vue'), meta: { login_required: true } },
      { path: '/selectDraft', component: () => import('pages/SelectDraft.vue'), meta: { login_required: true } },
      { path: '/search', component: () => import('pages/Search.vue'), meta: { login_required: true } },
      { path: '/userManager', component: () => import('pages/UserManager.vue'), meta: { sysadmin_required: true } },
      { path: '/import', component: () => import('pages/Import.vue'), meta: { login_required: true } },
      { path: '/export', component: () => import('pages/Export.vue'), meta: { login_required: true } }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes