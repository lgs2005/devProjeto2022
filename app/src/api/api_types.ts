export type User = {
    id: number,
    name: string,
    email: string,
}

export type Folder = {
    id: number,
    name: string,
    pages: Page[],
}

export type Page = {
    id: number,
    name: string,
    creation_date: Date,
    deletion_date: Date,
}