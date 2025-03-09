<template>
    <div>
        <div class="flex items-center md:px-2 pt-1 bg-base-200 md:bg-base-200">
            <div class="flex items-center md:bg-base-100 flex-1 rounded-xl md:mr-2 h-16 md:shadow-sm">
                <div class="ml-1 mr-auto indicator">
                    <div class="dropdown sm:hidden">
                        <div tabindex="0" role="button" class="btn btn-ghost btn-circle" @click="showSideBar">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                                 stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                      d="M4 6h16M4 12h16M4 18h7"/>
                            </svg>
                        </div>
                    </div>
                    <a class="btn btn-ghost normal-case text-xl">PhotoZen</a>
                </div>
                <div class="mr-auto !hidden md:!block">
                    <ul class="menu menu-horizontal px-1" v-if="role === 'V2'">
                        <li v-for="(item,index) in header.list" :key="index">
                            <a @click="redirectUrl(item)" :class="{ 'active': item.pathName === navName }">{{
                                    item.name
                                }}</a>
                        </li>
                    </ul>
                    <ul class="menu menu-horizontal px-1" v-else>
                        <li v-for="(item,index) in header.list" :key="index">
                            <a @click="redirectUrl(item)" :class="{ 'active': item.pathName === navName }"
                               v-if="role === item.role">{{ item.name }}</a>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="ml-auto md:bg-base-100 rounded-xl py-0.5 h-16 flex items-center md:shadow-sm">
                <div style="display: flex;justify-content: center;align-items: center;" class="md:mx-2">
                    <div class="relative" v-show="isSearch">
                        <div class="absolute w-72 -left-[250px] top-[46px] z-[11]">
                            <input type="text" ref="inputVal" class="input input-bordered input-sm w-full max-w-xs"
                                   placeholder="搜索关键词" v-model="searchTerm" @input="handleInput" autocomplete="off"
                                   @click="showResults=!showResults">
                            </input>
                            <ul class="absolute w-full bg-base-100 border border-base-100 rounded-md mt-2 shadow-lg"
                                v-if="showResults">
                                <div v-if="suggestions.artists.length > 0">
                                    <li class="ml-2 mt-2 text-base">艺术家</li>
                                    <li v-for="(artist, index) in suggestions.artists" :key="'at' + index"
                                        class="py-2 px-4 cursor-pointer hover:bg-gray-100 hover:rounded-lg"
                                        @click="redirectArtist(artist)">
                                        <div class="text-sm font-light">{{ artist.name }} -
                                            {{ artist.albumCount }}专辑
                                        </div>
                                    </li>
                                    <hr>
                                </div>
                                <div v-if="suggestions.albums.length > 0">
                                    <li class="ml-2 mt-2">专辑</li>
                                    <li v-for="(album, index) in suggestions.albums" :key="'al' + index"
                                        class="py-2 px-4 cursor-pointer hover:bg-gray-100 hover:rounded-lg"
                                        @click="redirectAlbum(album)">
                                        <div :key="'album' + index" class="text-sm font-light">
                                            {{ album.name }} - {{ album.year }} - {{ album.artist }}
                                        </div>
                                    </li>
                                    <hr>
                                </div>
                                <div v-if="suggestions.tracks.length > 0">
                                    <li class="ml-2 mt-2">歌曲</li>
                                    <li v-for="(track, index) in suggestions.tracks" :key="'tr' + index"
                                        class="py-2 px-4 cursor-pointer hover:bg-gray-100 hover:rounded-lg"
                                        @click="redirectTrack(track)">
                                        <div :key="'tra' + index" class="text-sm font-light">
                                            {{ track.title }} - {{ track.year }} - {{ track.artist }} - {{
                                                track.album
                                            }}
                                        </div>
                                    </li>
                                </div>
                            </ul>
                        </div>
                    </div>
                    <button class="btn btn-ghost btn-circle" @click="handleClick" v-if="role === 'V2'">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                             stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                        </svg>
                    </button>
                    <label class="swap swap-rotate">

                        <!-- this hidden checkbox controls the state -->
                        <input type="checkbox" @click="isShowTheme=true"/>

                        <!-- sun icon -->
                        <svg class="swap-on fill-current w-5 h-5" xmlns="http://www.w3.org/2000/svg"
                             viewBox="0 0 24 24">
                            <path
                                d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z"/>
                        </svg>

                        <!-- moon icon -->
                        <svg class="swap-off fill-current w-5 h-5" xmlns="http://www.w3.org/2000/svg"
                             viewBox="0 0 24 24">
                            <path
                                d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z"/>
                        </svg>

                    </label>
                    <div class="dropdown dropdown-end">
                        <label tabindex="0" class="btn btn-ghost btn-circle" @click="submitRecord">
                            <div class="indicator">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                                     stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                          d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
                                </svg>
                                <span class="badge badge-sm indicator-item badge-secondary"
                                      v-if="unreadCount !== 0">{{ unreadCount }}</span>
                            </div>
                        </label>
                        <div tabindex="0" class="mt-3 z-[1] card card-compact dropdown-content w-80 bg-base-100 shadow">
                            <div class="card-body overflow-y-auto">
                                <ul class="message-list flex flex-col">
                                    <li class="flex justify-between items-center cursor-pointer hover:bg-gray-100 my-2"
                                        v-for="(item,index) in msgList" :key="index">
                                        <div class="flex flex-col">
                                            <span class="text-xs text-gray-500">{{ item.title }}</span>
                                            <span class="text-xs text-gray-500">{{ item.content }}</span>
                                        </div>
                                        <span class="text-xs text-gray-500">{{ item.update_at }}</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="dropdown dropdown-end">
                        <label tabindex="0" class="btn btn-ghost btn-circle avatar">
                            <div class="w-10 rounded-full">
                                <img src="#"/>
                            </div>
                        </label>
                        <ul tabindex="0"
                            class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
                            <li class="nav-item" @click="handleUserListClic2k">
                                <a class="justify-between">
                                    后台管理
                                    <span class="badge">{{ username }}</span>
                                </a>
                            </li>
                            <li class="nav-item" @click="handleUserListClic3k">
                                <a class="justify-between">
                                    使用手册
                                    <span class="badge">v{{ version }}</span>
                                </a>
                            </li>
                            <li class="nav-item" @click="handleUserListClick">
                                <a class="justify-between">
                                    关于作者
                                    <span class="badge">{{ versionNum }}</span>
                                </a>
                            </li>
                            <li class="nav-item" @click="handleUserListClic4k">
                                <a>
                                    退出登录
                                    <span class="badge">Logout</span>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <div class="drawer">
            <input id="edit-show-bar" type="checkbox" class="drawer-toggle" v-model="isShowSideBar"/>
            <div class="drawer-content">
            </div>
            <div class="drawer-side z-20">
                <label for="edit-show-bar" aria-label="close sidebar" class="drawer-overlay"></label>
                <div class="p-4 min-h-full bg-base-100 text-base-content">
                    <Side/>
                </div>
            </div>
        </div>
        <div class="drawer drawer-end">
            <input id="drawer-theme" type="checkbox" class="drawer-toggle" v-model="isShowTheme"/>
            <div class="drawer-content">
                <!-- Page content here -->
            </div>
            <div class="drawer-side z-20">
                <label for="drawer-theme" aria-label="close sidebar" class="drawer-overlay"></label>
                <div class="p-8 w-80 min-h-full bg-base-200 text-base-content">
                    <div class="text-xl font-medium mb-1">切换主题: {{ currentTheme }}</div>
                    <div class="rounded-box grid grid-cols-1 gap-4">
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="light" data-act-class="!outline-base-content" @click="switchTheme('light')">
                            <div data-theme="light"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">light</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="dark" data-act-class="!outline-base-content" @click="switchTheme('dark')">
                            <div data-theme="dark"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">dark</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="cupcake" data-act-class="!outline-base-content"
                            @click="switchTheme('cupcake')">
                            <div data-theme="cupcake"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">cupcake</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="bumblebee" data-act-class="!outline-base-content"
                            @click="switchTheme('bumblebee')">
                            <div data-theme="bumblebee"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">bumblebee</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="emerald" data-act-class="!outline-base-content"
                            @click="switchTheme('emerald')">
                            <div data-theme="emerald"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">emerald</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="emerald" data-act-class="!outline-base-content"
                            @click="switchTheme('charles')">
                            <div data-theme="charles"
                                 class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">charles</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="corporate" data-act-class="!outline-base-content"
                            @click="switchTheme('corporate')">
                            <div data-theme="corporate"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">corporate</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="synthwave" data-act-class="!outline-base-content"
                            @click="switchTheme('synthwave')">
                            <div data-theme="synthwave"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">synthwave</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="retro" data-act-class="!outline-base-content" @click="switchTheme('retro')">
                            <div data-theme="retro"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">retro</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="cyberpunk" data-act-class="!outline-base-content"
                            @click="switchTheme('cyberpunk')">
                            <div data-theme="cyberpunk"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">cyberpunk</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="valentine" data-act-class="!outline-base-content"
                            @click="switchTheme('valentine')">
                            <div data-theme="valentine"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">valentine</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="halloween" data-act-class="!outline-base-content"
                            @click="switchTheme('halloween')">
                            <div data-theme="halloween"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">halloween</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="garden" data-act-class="!outline-base-content"
                            @click="switchTheme('garden')">
                            <div data-theme="garden"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">garden</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="forest" data-act-class="!outline-base-content"
                            @click="switchTheme('forest')">
                            <div data-theme="forest"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">forest</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="aqua" data-act-class="!outline-base-content" @click="switchTheme('aqua')">
                            <div data-theme="aqua"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">aqua</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="lofi" data-act-class="!outline-base-content" @click="switchTheme('lofi')">
                            <div data-theme="lofi"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">lofi</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="pastel" data-act-class="!outline-base-content"
                            @click="switchTheme('pastel')">
                            <div data-theme="pastel"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">pastel</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="fantasy" data-act-class="!outline-base-content"
                            @click="switchTheme('fantasy')">
                            <div data-theme="fantasy"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">fantasy</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="wireframe" data-act-class="!outline-base-content"
                            @click="switchTheme('wireframe')">
                            <div data-theme="wireframe"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">wireframe</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="black" data-act-class="!outline-base-content" @click="switchTheme('black')">
                            <div data-theme="black"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">black</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="luxury" data-act-class="!outline-base-content"
                            @click="switchTheme('luxury')">
                            <div data-theme="luxury"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">luxury</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="dracula" data-act-class="!outline-base-content"
                            @click="switchTheme('dracula')">
                            <div data-theme="dracula"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">dracula</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="cmyk" data-act-class="!outline-base-content" @click="switchTheme('cmyk')">
                            <div data-theme="cmyk"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">cmyk</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="autumn" data-act-class="!outline-base-content"
                            @click="switchTheme('autumn')">
                            <div data-theme="autumn"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">autumn</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="business" data-act-class="!outline-base-content"
                            @click="switchTheme('business')">
                            <div data-theme="business"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">business</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="acid" data-act-class="!outline-base-content" @click="switchTheme('acid')">
                            <div data-theme="acid"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">acid</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="lemonade" data-act-class="!outline-base-content"
                            @click="switchTheme('lemonade')">
                            <div data-theme="lemonade"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">lemonade</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="night" data-act-class="!outline-base-content" @click="switchTheme('night')">
                            <div data-theme="night"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">night</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="coffee" data-act-class="!outline-base-content"
                            @click="switchTheme('coffee')">
                            <div data-theme="coffee"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">coffee</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="winter" data-act-class="!outline-base-content"
                            @click="switchTheme('winter')">
                            <div data-theme="winter"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">winter</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="dim" data-act-class="!outline-base-content" @click="switchTheme('dim')">
                            <div data-theme="dim" class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">dim</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="nord" data-act-class="!outline-base-content" @click="switchTheme('nord')">
                            <div data-theme="nord"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">nord</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="border-base-content/20 hover:border-base-content/40 overflow-hidden rounded-lg border outline outline-2 outline-offset-2 outline-transparent"
                            data-set-theme="sunset" data-act-class="!outline-base-content"
                            @click="switchTheme('sunset')">
                            <div data-theme="sunset"
                                class="bg-base-100 text-base-content w-full cursor-pointer font-sans">
                                <div class="grid grid-cols-5 grid-rows-3">
                                    <div class="bg-base-200 col-start-1 row-span-2 row-start-1"></div>
                                    <div class="bg-base-300 col-start-1 row-start-3"></div>
                                    <div
                                        class="bg-base-100 col-span-4 col-start-2 row-span-3 row-start-1 flex flex-col gap-1 p-2">
                                        <div class="font-bold">sunset</div>
                                        <div class="flex flex-wrap gap-1" data-svelte-h="svelte-1kw79c2">
                                            <div
                                                class="bg-primary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-primary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-secondary flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-secondary-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-accent flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-accent-content text-sm font-bold">A</div>
                                            </div>
                                            <div
                                                class="bg-neutral flex aspect-square w-5 items-center justify-center rounded lg:w-6">
                                                <div class="text-neutral-content text-sm font-bold">A</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <input type="checkbox" id="my_modal_6" class="modal-toggle" v-model="showActiceCode"/>
            <div class="modal" role="dialog">
                <div class="modal-box">
                    <div v-if="!isForever">
                        <h3 class="font-bold text-lg" v-if="role === 'V1'">激活 V2 版本</h3>
                        <h3 class="font-bold text-lg" v-else>升级 V2 永久版本</h3>
                        <label class="form-control w-full max-w-xs mt-4">
                            <div class="label">
                                <span class="label-text">输入你的激活码：</span>
                            </div>
                            <input type="text" placeholder="请输入" class="input input-bordered w-full max-w-xs"
                                   v-model="code"/>
                            <div class="mt-1 label-text text-gray-400 underline cursor-pointer" @click="redirectAfdian">获取激活码？</div>
                        </label>
                        <div class="modal-action">
                            <label for="my_modal_6" class="btn btn-md btn-neutral" @click="handleActiveCode">激活</label>
                            <label for="my_modal_6" class="btn btn-md">关闭</label>
                        </div>
                    </div>
                    <div v-else>
                        您已经是永久激活用户！
                        <div class="modal-action">
                            <label for="my_modal_6" class="btn btn-md">关闭</label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script lang="ts" setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useSearchStore } from '@/stores/search'
import { clearStore } from '../../common/store.js'
// @ts-ignore
import Side from './side.vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const searchStore = useSearchStore()

const logout_url = ref('https://github.com/xhongc/music-tag-web')
const pageTitle = ref('测试')
const currentTheme = ref('light')
const userData = ref({})
const role = ref('')
const isForever = ref(false)
const username = ref('')
const msgList = ref<Array<{title: string, content: string, update_at: string}>>([])
const unreadCount = ref(0)
const showResults = ref(false)
const isSearch = ref(false)
const searchTimeout2 = ref<ReturnType<typeof setTimeout> | null>(null)
const suggestions = ref({
  artists: [] as Array<{name: string, albumCount: number}>,
  albums: [] as Array<{name: string, year: string, artist: string}>,
  tracks: [] as Array<{title: string, year: string, artist: string, album: string}>
})
const syncSwitch = ref(true)
const showActiceCode = ref(false)
const inputVal = ref<HTMLInputElement | null>(null)

const user = ref({
  list: ['关于作者']
})

const header = ref({
  list: [
    {
      name: '首页',
      id: 3,
      show: true,
      pathName: 'home',
      role: 'V2'
    },
    {
      name: '照片', 
      id: 1,
      show: true,
      pathName: 'photos',
      role: 'V1'
    },
    {
      name: '相册',
      id: 6, 
      show: true,
      pathName: 'albums',
      role: 'V1'
    },
    {
      name: '文件',
      id: 4,
      show: true, 
      pathName: 'file',
      role: 'V2'
    },
    {
      name: '探索',
      id: 2,
      show: true,
      pathName: 'expore', 
      role: 'V2'
    },
    {
      name: '设置',
      id: 5,
      show: true,
      pathName: 'settings',
      role: 'V2'
    }
  ],
  active: -1
})

const code = ref('')
const isShowSideBar = ref(false)
const isShowTheme = ref(false)

const colorMap: Record<string, string> = {
  'light': '#f2f2f2',
  'dark': '#1a1e23',
  'cupcake': '#eeeae6',
  'bumblebee': '#e8e8e8',
  'emerald': '#e8e8e8',
  'corporate': '#e8e8e8',
  'synthwave': '#150e34',
  'retro': '#e2d8b8',
  'cyberpunk': '#e7dc5f',
  'valentine': '#e0d2dd',
  'halloween': '#1d1d1d',
  'garden': '#d3d2d2',
  'forest': '#130f0f',
  'aqua': '#375393',
  'lofi': '#f2f2f2',
  'pastel': '#f9fafb',
  'fantasy': '#e8e8e8',
  'wireframe': '#eeeeee',
  'black': '#141414',
  'luxury': '#171618',
  'dracula': '#24252f',
  'cmyk': '#e8e8e8',
  'autumn': '#dbdbdb',
  'business': '#1c1c1c',
  'acid': '#e3e3e3',
  'lemonade': '#e2e6da',
  'night': '#0e1424',
  'coffee': '#1b131b',
  'winter': '#f3f7fe',
  'dim': '#252932',
  'nord': '#e6e9ef',
  'sunset': '#10171d'
}

const refresh = computed(() => {
  if (userStore.hasMsg) {
    userStore.setHasMsg(false)
    fetchRecord()
  }
})

const searchTerm = computed({
  get: () => searchStore.searchTerm,
  set: (value) => searchStore.setSearchTerm(value)
})

const headerTitle = computed(() => route.meta.title)

const navName = computed(() => {
  return route.meta.hasOwnProperty('fatherName') ? route.meta.fatherName : route.name
})

declare global {
  interface Window {
    projectVersion: string;
    projectVersionNum: string;
  }
}

const version = computed(() => window.projectVersion)

const versionNum = computed(() => window.projectVersionNum)

const isHiddenBGP = computed({
  get: () => window.localStorage.getItem('isHiddenBGP') === 'true',
  set: (value) => window.localStorage.setItem('isHiddenBGP', value ? 'true' : 'false')
})

onMounted(() => {
  loginUser()
  initTheme()
  fetchRecord()
})

const initTheme = () => {
  if (localStorage.getItem('theme')) {
    currentTheme.value = localStorage.getItem('theme') as string
  }
  document.documentElement.setAttribute('data-theme', currentTheme.value)
  localStorage.setItem('theme', currentTheme.value)
  
  let metaThemeColor = document.querySelector('meta[name="theme-color"]')
  if (metaThemeColor) {
    metaThemeColor.setAttribute('content', colorMap[currentTheme.value])
  }
}

const switchTheme = (theme: string) => {
  currentTheme.value = theme
  document.documentElement.setAttribute('data-theme', currentTheme.value)
  localStorage.setItem('theme', currentTheme.value)
  
  let metaThemeColor = document.querySelector('meta[name="theme-color"]')
  if (metaThemeColor) {
    metaThemeColor.setAttribute('content', colorMap[currentTheme.value])
  }
}

// 添加缺失的功能函数
const showSideBar = () => {
  isShowSideBar.value = !isShowSideBar.value
}

const redirectUrl = (item: any) => {
  router.push({ name: item.pathName })
}

const handleInput = () => {
  if (searchTimeout2.value) {
    clearTimeout(searchTimeout2.value)
  }
  
  searchTimeout2.value = setTimeout(() => {
    if (searchTerm.value && searchTerm.value.length > 1) {
      fetchSuggestions()
    } else {
      suggestions.value = {
        artists: [],
        albums: [],
        tracks: []
      }
    }
  }, 300)
}

const fetchSuggestions = async () => {
  try {
    const response = await searchStore.searchSuggestions(searchTerm.value)
    if (response.result) {
      suggestions.value = response.data
    }
  } catch (error) {
    console.error('搜索建议获取失败:', error)
  }
}

const redirectArtist = (artist: any) => {
  router.push({ name: 'artist', params: { id: artist.id } })
  showResults.value = false
}

const redirectAlbum = (album: any) => {
  router.push({ name: 'album', params: { id: album.id } })
  showResults.value = false
}

const redirectTrack = (track: any) => {
  router.push({ name: 'track', params: { id: track.id } })
  showResults.value = false
}

const handleClick = () => {
  isSearch.value = !isSearch.value
  if (isSearch.value) {
    nextTick(() => {
      inputVal.value?.focus()
    })
  }
}

const submitRecord = async () => {
  await fetchRecord()
}

const fetchRecord = async () => {
  try {
    const res = await userStore.getNotifications()
    if (res.result) {
      msgList.value = res.data.list
      unreadCount.value = res.data.unread_count
    }
  } catch (error) {
    console.error('获取通知失败:', error)
  }
}

const handleUserListClick = () => {
  window.open(logout_url.value, '_blank')
}

const handleUserListClic2k = () => {
  router.push({ name: 'admin' })
}

const handleUserListClic3k = () => {
  router.push({ name: 'manual' })
}

const handleUserListClic4k = () => {
  clearStore()
  router.push({ name: 'login' })
}

const redirectAfdian = () => {
  window.open('https://afdian.net/@xhongc', '_blank')
}

const handleActiveCode = async () => {
  if (!code.value) {
    return
  }
  
  try {
    const res = await userStore.activeCode(code.value)
    if (res.result) {
      isForever.value = true
      showActiceCode.value = false
    } else {
      alert(res.msg || '激活失败')
    }
  } catch (error) {
    console.error('激活失败:', error)
  }
}

// 添加缺失的Cookie处理函数
const setCookie = (name: string, value: string, days: number) => {
  const date = new Date()
  date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000))
  const expires = "expires=" + date.toUTCString()
  document.cookie = name + "=" + value + ";" + expires + ";path=/"
}

const loginUser = async () => {
  try {
    const res = await userStore.loginInfo()
    if (res.result) {
      userData.value = res.data
      role.value = res.data.role
      isForever.value = res.data.is_forever
      username.value = res.data.username
      userStore.setUserRole(res.data.role)
      userStore.setUsername(res.data.username)
      setCookie('username', res.data.username, 7)
      setCookie('salt', res.data.salt, 7)
      setCookie('hash', res.data.hash, 7)
      window.localStorage.setItem('mi_play_in_pl', res.data.sys_dict.mi_play_in_pl)
    } else {
      router.push({name: 'login'})
    }
  } catch (error) {
    console.error(error)
  }
}
</script>

<style scoped>
/* Styles remain unchanged */
</style>

<style>
/* Global styles remain unchanged */
</style>
