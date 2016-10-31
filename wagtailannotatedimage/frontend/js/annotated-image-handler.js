class AnnotatedImageEditHandler {
	constructor(container, imageFieldId) {
		this.container = container;
		this.imageFieldId = imageFieldId;
		this.formPrefix = 'annotation-'
		this._index = 1;
		this._annotationData = {};
		this.annotationsField = $(container).find('[data-annotations-field] input');
		this.imageContainer = $(container).find('[data-image-container]');
	}

	get index() {
		return this._index;
	}

	set index(index) {
		this._index = index
	}

	get annotationData() {
		return this._annotationData;
	}

	set annotationData(data) {
		this._annotationData = data;
		this.annotationsField.val(JSON.stringify(data));
	}

	setUp() {
		var img = this.imageContainer.find('img');
		if(img.length > 0) {
			this.imageContainer.annotatableImage(this.createAnnotation.bind(this));
		}

		if(this.annotationsField.val() && this.annotationsField.val() != '{}') {
			var annotations = JSON.parse(this.annotationsField.val());
			this.annotationData = annotations;

			var toAdd = []
			var index = 0;
			for(var key in annotations) {
				var annotationObj = annotations[key];
				annotationObj['id'] = key
				if(key >= index) {
					index = parseInt(key) + 1;
				}
				toAdd.push(annotationObj);
				this.createAnnotationForm(key, annotations[key]);
			}
			this.index = index;
			this.imageContainer.find('img').load(function(){
				this.imageContainer.addAnnotations(function(annotation){
					var annotationElement =  $(document.createElement('span'));
					annotationElement.addClass('note');
					annotationElement.html(annotation.id);
					annotationElement.attr('data-annotation-id', annotation.id);
					return annotationElement;
				}, toAdd);
			}.bind(this))
		}

		this.attachObserver();
	}

	attachObserver() {
		new MutationObserver( function(mutations) {
			mutations.forEach(function(mutation){
				if(mutation.attributeName === 'value') {
					var imageId = mutation.target.value;
					var image = this.container.find('img');
					if(image != null) {
						this.reset();
					}
					if(imageId) {
						$.get(window.location.origin + '/admin/full_image/' + imageId,
							function(data) {
								this.imageContainer.html(data);
								this.imageContainer.annotatableImage(this.createAnnotation.bind(this));
							}.bind(this)
						)
					}
				}
			}.bind(this));
		}.bind(this))
		.observe(this.container[0].querySelector('#' + this.imageFieldId), { attributes: true });
	}

	createAnnotation() {
		var index = this.index;
		var annotationElement =  $(document.createElement('span'));
		annotationElement.addClass('note');
		annotationElement.attr('data-annotation-id', index);
		annotationElement.html(index);
		this.createAnnotationForm(index, null);
		this.addAnnotationEntry(index, annotationElement);
		index++;
		this.index = index;
		return annotationElement;
	}

	reset() {
		this.index = 1;
		this.annotationData = {};
		this.imageContainer.empty();
		this.container.find('[data-annotation-forms]').empty();
	}

	createAnnotationForm(index, initialData) {
		var annotationForm = this.container.find('[data-annotation-form]').clone(false);
		annotationForm.removeAttr('data-annotation-form');
		annotationForm.find('[name="' + this.formPrefix + 'annotation_number"]').val(index);
		annotationForm.prepend('<button href="#" class="button icon text-replace hover-no icon-bin" data-delete="' + index + '"></button>')
		annotationForm.prepend('<h3>' + index + '</h3>');
		annotationForm.find('button').click(this.deleteAnnotationHandler.bind(this));
		if(initialData && Object.keys(initialData.fields).length > 0) {
			var fields = initialData.fields;
			for(name in fields) {
				//input
				var input = annotationForm.find('[name="' + this.formPrefix + name +'"]');
				if(input.length > 0){
					input.val(fields[name])
				}
			}
		}

		annotationForm.find('input, textarea, select').change(this.annotationFieldHandler.bind(this));
		this.container.find('[data-annotation-forms]').append(annotationForm);
	}

	addAnnotationEntry(index, annotationElement) {
		// small timeout so that position is taken AFTER the annotation is added
		setTimeout(function() {
			var annotations = this.annotationData;
			var annotationPos = annotationElement.seralizeAnnotations()[0]
			annotations[index] = {
				x: annotationPos.x,
				y: annotationPos.y,
				fields: {}
			}
			this.annotationData = annotations;
		}.bind(this), 100);
	}

	deleteAnnotationHandler(event) {
		event.preventDefault();
		var target = event.target;
		var id = target.dataset['delete'];
		var annotations = this.annotationData;
		delete annotations[id];
		target.parentNode.remove();
		this.imageContainer.find('[data-annotation-id="' + id + '"]').remove();
		this.annotationData = annotations;
	}

	annotationFieldHandler(event) {
		var target = event.target;
		var parent = target.parentNode.parentNode;
		var id = parent.querySelector('[name="' + this.formPrefix + 'annotation_number"]').value
		var annotations = this.annotationData;
		var fieldName = target.name.substring(this.formPrefix.length);
		annotations[id]['fields'][fieldName] = target.value;
		this.annotationData = annotations;
	}
}
