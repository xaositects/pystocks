var Files = {
    container: '',
    total_folders: 0,
    folder_state: 'closed',
    div_to_notify: '',
    activate_chooser: false,
    single_file: false,
    selected_files: [],
    InitChooser: function (id, single_file) {
        Files.activate_chooser = true;
        Files.single_file = true;
        Files.Folders(id, '0');
    },
    Init: function (container) {
        Files.container = container;
        Files.Folders(container, '', '/');
    },
    GetSelectedFiles: function () {
        return Files.selected_files;
    },
    SetFolderState: function (container, state) {
        $('#' + container).data('state', state);
    },
    GetFolderState: function (container) {
        return $('#' + container).data('state');
    },
    FolderCloseAction: function (container) {
        return function () {
            $(container).hide();
        };
    },
    FolderOpenAction: function (container, id, path) {
        return function () {
            if (Files.GetFolderState(container) === 'closed') {
                Files.SetFolderState(container, 'open');
                $('#folder_icon_' + id).html('folder_open');
                Files.Folders(container, id, path);
                Files.Files(id, path);
            } else {
                $('#folder_icon_' + id).html('folder');
                $('#' + container).html('');
                $('#ci_' + id + ' > li.collection-item').remove();
                Files.SetFolderState(container, 'closed');
            }
        };
    },
    FolderDownloadAction: function (id, uid) {
        return function () {
            window.open('/?action=download_folder&id=' + id + '&uid=' + uid);
        };
    },
    Folders: function (container, id, path) {
        if (container === '') {
            $('#' + container).prepend('<ul class="collection" id="master_parent_' + container + '"></ul>');
        } else {
            $('#' + container).append('<iframe class="hide" id="file_opener" name="file_opener"></iframe><ul class="collection" id="master_parent_' + container + '"></ul>');
        }

        if (container !== '') {
            $('#folder_icon_' + container).html('folder_open');
        }

        $.ajax({
            url: '/Documents/getFolders',
            data: {
                path: path
            },
            dataType: 'json',
            type: 'post',
            success: function (r) {
                Files.WriteFolderList(container, id, r);
            },
            error: function (r) {
                console.log(r);
                Materialize.toast('There was an error getting the folder list.', 5000);
            }
        });
    },
    WriteFolderList: function (container, id, r) {
        if(!id) {
            id = container;
        }
        for (var i in r) {
            if ($('#ci_' + id).find('#sl_' + r[i].id).length === 0) {
                var fc = '<li class="collection-item" id="ci_' + r[i].id + '"><i class="material-icons left click" id="folder_icon_' + r[i].id + '" >folder</i><span id="fn_' + r[i].id + '">' + r[i].name + '</span><div data-state="closed" id="sl_' + r[i].id + '"></div></li>';
                //if no parent, assign to master list, else assign to the parent
                if (id === 0 || id === null || !id || id === '0' || id === Files.container) {
                    $('#master_parent_' + id).append(fc);
                } else {
                    $('#ci_' + id + ' #sl_' + id).after(fc);
                    
                }
                $('#folder_icon_' + r[i].id).click(Files.FolderOpenAction('sl_' + r[i].id, r[i].id, r[i].path));
                $('#folder_download_' + r[i].id).click(Files.FolderDownloadAction(r[i].id));
            }

        }
    },
    FileDownloadAction: function (id) {
        return function () {
            window.open('/?action=download_file&id=' + id);
        };
    },
    FileOpenAction: function (file) {
        return function () {
            window.open('/Documents/openFile/' + encodeURI(file), 'file_opener');
        };
    },
    FileSelectAction: function (id) {
        return function () {
            if ($('#file_select_' + id).prop('checked')) {
                Files.selected_files.push(id);
                if (Files.div_to_notify) {
                    if (Files.single_file === true) {
                        $('#' + Files.div_to_notify).empty().prepend('<li class="collection-item">' + $('#file_select_' + id).data('filename') + '</li>');
                    } else {
                        $('#' + Files.div_to_notify).prepend('<li class="collection-item">' + $('#file_select_' + id).data('filename') + '</li>');
                    }
                }
            } else {
                var f = Files.selected_files.indexOf(id);
                Files.selected_files.splice(f, 1);
                if (Files.div_to_notify) {
                    var fhtml = $('#' + Files.div_to_notify).html();
                    var to_add = '<li class="collection-item">' + $('#file_select_' + id).data('filename') + '</li>';
                    fhtml = fhtml.replace(to_add, "");
                    $('#' + Files.div_to_notify).html(fhtml);
                }
            }
        };
    },
    Files: function (folder_id, path) {
        $('#sl_' + folder_id).empty().append('<ul class="collection" id="files_' + folder_id + '"></ul>');
        $.ajax({
            url: '/Documents/getFiles',
            data: {
                
                path: path
            },
            dataType: 'json',
            type: 'post',
            success: function (r) {
                if (r.length > 0) {
                    for (var i in r) {
                        var file_icon;
                        switch (true) {
                            case / image | jp?eg | png | gif / .test(r[i].type):
                                file_icon = 'image';
                                break;
                            case / pdf / .test(r[i].type):
                                file_icon = 'picture_as_pdf';
                                break;
                            default:
                                file_icon = 'insert_drive_file';
                        }
                        var fn = (r[i].file_name ? r[i].file_name : r[i].id + '.' + r[i].type);
                        $('#files_' + folder_id).append('<li class="collection-item" id="file_' + r[i].id + '">' + ((Files.activate_chooser === true) ? '<input type="checkbox" data-filename="' + fn + '" id="file_select_' + r[i].id + '" /><label for="file_select_' + r[i].id + '"><i class="material-icons left" id="file_icon_' + r[i].id + '" >' + file_icon + '</i>' + fn + '</label>' : '<span class="click" id="file_open_' + r[i].id + '"><i class="material-icons left" id="file_icon_' + r[i].id + '" >' + file_icon + '</i>' + (r[i].file_name ? r[i].file_name : r[i].uid + '.' + r[i].type) + '</span>') + '</li>');
                        $('#file_download_' + r[i].id).click(Files.FileDownloadAction(r[i].id, r[i].uid));
                        $('#file_open_' + r[i].id).click(Files.FileOpenAction(r[i].path));
                    }
                }
            }
        });
    },
    setFolderTooltips: function () {
        $('.folder-title').each(function () {
            addTT($(this).attr('id'), $(this).attr('title'));
        });
    }
};

