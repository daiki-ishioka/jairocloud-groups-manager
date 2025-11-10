interface Repository {
  id: string
  displayName: string
  url: string
  entityIds: string
  suspended: boolean
}

interface Group {
  id: string
  displayName: string
  isPublic: boolean
  joinCondition: 'open' | 'approval' | 'invite-only'
  memberVisibility: 'public' | 'private' | 'hidden'
  members?: Pick<User, 'id'>[]
}

interface User {
  id: string
  displayName: string
  role?: string[]
  email?: string
  eppn: string
  lastModified: string
}

export type { Repository, Group, User }
