/*
 * Copyright (C) 2026 National Institute of Informatics.
 */

/**
 * Composable to manage the application menu items
 */
export function useMenu() {
  const management = [
    { label: 'Repositories', to: '/repositories' },
    { label: 'Groups', to: '/groups' },
    { label: 'Users', to: '/users' },
  ]
  const other = [
    { label: 'History', to: '/history' },
    { label: 'Cache Groups', to: '/cache-groups' },
  ]

  return {
    management,
    other,
  }
}
