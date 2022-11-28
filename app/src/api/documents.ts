import { Folder, Page } from "./api_types";
import fetch2b from "./fetch2b";

export function api_doclistFull() {
    return fetch2b<Folder[]>('/api/docs/doclist', 'GET');
}

export function api_doclist(folder_id: number) {
    return fetch2b<Folder>(`/api/docs/${folder_id}`, 'GET');
}

export function api_newFolder(name: string) {
    return fetch2b<Folder>('/api/docs/folder/new', 'POST', { name });
}

export function api_newDocument(name: string, folder_id: number) {
    return fetch2b<Page>(`/api/docs/${folder_id}/new`, 'POST', { name });
}