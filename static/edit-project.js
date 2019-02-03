$(function(){

    function capitalize(string){
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
    
    function get_new_version_changes(){
        version_form = $('#version-form');
        ul_s = version_form.find('ul');
    
        changes = {}
    
        for(ul of ul_s){
            ul = $(ul);
            change_type = ul.parent().attr('id');
            changes[change_type] = [];
            li_s = ul.find('li');
            for(li of li_s){
                li = $(li)
                val = li.html().trim()
                changes[change_type].push(val)
            }
        }
    
        return changes
    
    }

    function new_version(){
        if ($('#version-form #number-of-new-version').val()){
            data = {
                'version_number': $('#version-form #number-of-new-version').val(),
                'cretical'      : $('#version-form #cretical').is(":checked"),
                'combitable'    : $('#version-form #combitable').is(":checked"),
                'changes'       : get_new_version_changes(),
            }

            return data
        }
        return false
    }
    
    function get_editted_changes_in_old_versions(){
        // get changes binding to its id
        editted_changes = $('.old-version li.editted');
        editted_changes_data = {}
        for(change of editted_changes){
            change = $(change)
            version_id  = change.parentsUntil('.old-version').parent().attr('version-id');

            if(editted_changes_data.hasOwnProperty(version_id)){
                editted_changes_data[version_id].push({
                    'val': change.html(), 
                    'id' : change.attr('change-id'),
                })
            }else{
                editted_changes_data[version_id] = [{
                    'val': change.html(), 
                    'id' : change.attr('change-id'),
                }]
            }
        }
    
        return editted_changes_data
    }


    function get_new_changes_in_old_versions(){
        new_changes = $('.old-version li.version-change');
        new_changes_data = {};
        for(change of new_changes){
            change      = $(change)
            change_type = change.parent().siblings('div:first').find(':first').text().toLowerCase()
            version_id  = change.parentsUntil('.old-version').parent().attr('version-id');
            
            if(new_changes_data.hasOwnProperty(version_id)){
                new_changes_data[version_id].push({
                    'val': change.html(), 
                    'type': change_type,
                })
            }else{
                new_changes_data[version_id] = [{
                    'val': change.html(), 
                    'type': change_type,
                }]
            }
        }
        return new_changes_data
    }


    function get_editted_meta_data_in_old_versions(){
        old_versions = $('.old-version');
        editted_meta_data = {}
        for (version of old_versions){
            version = $(version);
            version_id = version.attr('version-id');
            if (version.find(':first').find('.editted').length > 0){
                meta = version.find(':first') // first row contain my meta
                editted_meta_data[version_id] = {
                    'version_number': meta.find(':first').text(),
                    'cretical'      : meta.find('input[type="checkbox"]').first().is(":checked"),
                    'combitable'    : meta.find('input[type="checkbox"]').last().is(":checked"),
                }
            }
        }
        return editted_meta_data
    }

    function old_version(){
        if($('.old-version .editted, .old-version .version-change').length > 0){
            data = {
                'editted_meta_data': get_editted_meta_data_in_old_versions(),
                'editted_changes'  : get_editted_changes_in_old_versions(),
                'added_changes'    : get_new_changes_in_old_versions(),
            }
            return data
        }
        return false
    }


    var AddVersionBtn = $('#add-version'),
        version_form  = $('#version-form'),
        change_types  = $('#change-types'),
        change_format = $('#added'),
        insert_change_form = $('#input-change'),
        add_change= insert_change_form.find('#submit-change');

    // 1 - remove formats in order
    insert_change_form.remove();
    change_format.remove();
    version_form.remove();

    // 2 - handle events
    AddVersionBtn.click((e)=>{
        // version_form.insertBefore('.old-version:first')
        version_form.insertAfter('#area-of-add-version');
        // $('.container').append(version_form);
        $(e.target).off('click');
    });

    change_types.change(()=>{
        val = change_types.val();
        Val = capitalize(val);
        change_types.find('#temp').remove()

        
        if( $('#' + val).length > 0 ){
            // chane type already exist
        }
        else{
            clone = change_format.clone()
            clone.attr('id', val);
            clone.find('.title').text(Val)

            clone.append(insert_change_form)
            version_form.append(clone)
        }
    });

    version_form.on('click', '.get-input-change-from', (event)=>{
        $(event.target).parent().parent().append(insert_change_form);
    });

    $('.get-input-change-from').click((event)=>{
        $(event.target).parent().parent().append(insert_change_form);
    });

    add_change.click( (event)=>{
        elm   = event.target;
        // input = $(elm).siblings('input')
        input = $(elm).siblings('#rich-box').find('textarea')
        val   = input.val()
        ul    = $(elm).parent().siblings('ul');
        if (val){
            li = $('<li />').html(val)
            li.attr('class', 'version-change')
            ul.append( li )
            input.val('').trigger('keyup')
        }
    });

    var elm_edit_on_dblclick = [
        '#project-name', 
        '#project-brief',
        '#version-form .version-change',
        '.old-version .version-changes li[change-id]',
        '.version-number span:first-of-type',
    ];
    elms = elm_edit_on_dblclick.join(', ');
    
    $('body').on('dblclick', elms, (e)=>{
        content = $(e.target).text();

        $('body').css('overflow', 'hidden')
        
        // create prompt box to take new input from him
        cover = $('<div />').attr('id', 'cover').css({
            position: 'fixed',
            width: '100%',
            height: '100%',
            top: 0,
            left: 0,
            'background-color': '#212121b8'
        }).click(()=>{
            new_value = $('#cover-input').val();
            old_value = $(e.target).text();
            if(new_value != old_value){
                $(e.target).text( new_value ).addClass('editted')
            }
            $('#cover, #cover-input').remove();
            $('body').css('overflow', 'auto');
        });
        
        input = $('<textarea />').attr('id', 'cover-input').val(content).css({
            'min-width': '50%',
            'min-height': '70%',
            position: 'fixed',
            left: '25%',
            top: '50%',
            transform: 'translateY(-50%)',
            'font-size': '1.2em',
            'background-color': '#333',
            border: '1px solid',
            color: '#FFF',
            padding: '22px 0 22px 22px',
            'font-weight': 900,
        });

        $('body').append(cover)
        $('body').append(input);
    });
    
    $('.old-version ul').slideUp()
    $('.old-version .collabse-changes').click( (e)=>{
        $(e.target).parent().siblings('ul').slideToggle('slow')
    });

    $('.old-version input[type="checkbox"]').change((e)=>{
        x = $(e.target).addClass('editted').siblings().text().trim()
        if (x == '(cretical)'){
            $(e.target).siblings().text('(not cretical)').css('color', 'green')
        }else if(x == '(not cretical)'){
            $(e.target).siblings().text('(cretical)').css('color', 'red')
        }else if (x == '(combitable)'){
            $(e.target).siblings().text('(not combitable)').css('color', 'red')
        }else if(x == '(not combitable)'){
            $(e.target).siblings().text('(combitable)').css('color', 'green')
        }        
    });

    $('form input[type="button"]').click((e)=>{
        var data = {
            'project_data':{
                'project_name': $('#project-name').text(),
                'brief'       : $('#project-brief').text(),
                'worked_on'   : $('#worked-on').is(":checked"),
                'can_try'     : $('#can-try').is(":checked"),
                'finished'    : $('#finished').is(":checked"),
            },
            'new_version' : new_version(),
            'old_version' : old_version(),
        };
        console.log(data)
        data = JSON.stringify(data);
        $('form #data').val(data);
        $('form').submit();

    });
})