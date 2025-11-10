import data from './data.json'

export function useDataStore() {
  return {
    repositories: data.repositories as Repository[],
    groups: data.groups as Group[],
    users: data.users as User[],
  }
}
