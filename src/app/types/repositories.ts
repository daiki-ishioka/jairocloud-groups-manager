/**
 * Types related to repositories
 */

/** Repository summary information */
interface RepositorySummary {
  id: string
  serviceName: string
  serviceUrl: string
  spConnectorId?: string
  entityIds?: string[]
}

/** Repository detailed information */
interface RepositoryDetail extends RepositorySummary {
  suspended?: boolean
  serviceId?: string
  created?: Date
  lastModified?: Date
  usersCount?: number
  groupsCount?: number
}

export type { RepositorySummary, RepositoryDetail }
