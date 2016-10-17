'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var AnnotatedImageEditHandler = function () {
	function AnnotatedImageEditHandler(container, imageFieldId) {
		_classCallCheck(this, AnnotatedImageEditHandler);

		this.container = container;
		this.imageFieldId = imageFieldId;
		this._index = 1;
		this._annotationData = {};
		this.annotationsField = $(container).find('[data-annotations-field] input');
		this.imageContainer = $(container).find('[data-image-container]');
	}

	_createClass(AnnotatedImageEditHandler, [{
		key: 'setUp',
		value: function setUp() {
			var img = this.imageContainer.find('img');
			if (img.length > 0) {
				this.imageContainer.annotatableImage(this.createAnnotation.bind(this));
			}

			if (this.annotationsField.val() && this.annotationsField.val() != '{}') {
				var annotations = JSON.parse(this.annotationsField.val());
				this.annotationData = annotations;

				var toAdd = [];
				var index = 0;
				for (var key in annotations) {
					var annotationObj = annotations[key];
					annotationObj['id'] = key;
					if (key >= index) {
						index = parseInt(key) + 1;
					}
					toAdd.push(annotationObj);
					this.createAnnotationForm(key, annotations[key]);
				}
				this.index = index;
				this.imageContainer.find('img').load(function () {
					this.imageContainer.addAnnotations(function (annotation) {
						var annotationElement = $(document.createElement('span'));
						annotationElement.addClass('note');
						annotationElement.html(annotation.id);
						annotationElement.attr('data-annotation-id', annotation.id);
						return annotationElement;
					}, toAdd);
				}.bind(this));
			}

			this.attachObserver();
		}
	}, {
		key: 'attachObserver',
		value: function attachObserver() {
			new MutationObserver(function (mutations) {
				mutations.forEach(function (mutation) {
					if (mutation.attributeName === 'value') {
						var imageId = mutation.target.value;
						var image = this.container.find('img');
						if (image != null) {
							this.reset();
						}
						if (imageId) {
							$.get(window.location.origin + '/admin/full_image/' + imageId, function (data) {
								this.imageContainer.html(data);
								this.imageContainer.annotatableImage(this.createAnnotation.bind(this));
							}.bind(this));
						}
					}
				}.bind(this));
			}.bind(this)).observe(this.container[0].querySelector('#' + this.imageFieldId), { attributes: true });
		}
	}, {
		key: 'createAnnotation',
		value: function createAnnotation() {
			var index = this.index;
			var annotationElement = $(document.createElement('span'));
			annotationElement.addClass('note');
			annotationElement.attr('data-annotation-id', index);
			annotationElement.html(index);
			this.createAnnotationForm(index, null);
			this.addAnnotationEntry(index, annotationElement);
			index++;
			this.index = index;
			return annotationElement;
		}
	}, {
		key: 'reset',
		value: function reset() {
			this.index = 1;
			this.annotationData = {};
			this.imageContainer.empty();
			this.container.find('[data-annotation-forms]').empty();
		}
	}, {
		key: 'createAnnotationForm',
		value: function createAnnotationForm(index, initialData) {
			var annotationForm = this.container.find('[data-annotation-form]').clone(false);
			annotationForm.removeAttr('data-annotation-form');
			annotationForm.find('#id_annotation_number').val(index);
			annotationForm.prepend('<button href="#" class="button icon text-replace hover-no icon-bin" data-delete="' + index + '"></button>');
			annotationForm.prepend('<h3>' + index + '</h3>');
			annotationForm.find('button').click(this.deleteAnnotationHandler.bind(this));
			if (initialData && Object.keys(initialData.fields).length > 0) {
				var fields = initialData.fields;
				for (name in fields) {
					//input
					var input = annotationForm.find('input[name="' + name + '"]');
					if (input.length > 0) {
						input.val(fields[name]);
					} else {
						var select = annotationForm.find('select').val(fields[name]);
					}
				}
			}

			annotationForm.find('input, select').change(this.annotationFieldHandler.bind(this));
			this.container.find('[data-annotation-forms]').append(annotationForm);
		}
	}, {
		key: 'addAnnotationEntry',
		value: function addAnnotationEntry(index, annotationElement) {
			// small timeout so that position is taken AFTER the annotation is added
			setTimeout(function () {
				var annotations = this.annotationData;
				var annotationPos = annotationElement.seralizeAnnotations()[0];
				annotations[index] = {
					x: annotationPos.x,
					y: annotationPos.y,
					fields: {}
				};
				this.annotationData = annotations;
			}.bind(this), 100);
		}
	}, {
		key: 'deleteAnnotationHandler',
		value: function deleteAnnotationHandler(event) {
			event.preventDefault();
			var target = event.target;
			var id = target.dataset['delete'];
			var annotations = this.annotationData;
			delete annotations[id];
			target.parentNode.remove();
			this.imageContainer.find('[data-annotation-id="' + id + '"]').remove();
			this.annotationData = annotations;
		}
	}, {
		key: 'annotationFieldHandler',
		value: function annotationFieldHandler(event) {
			var target = event.target;
			var parent = target.parentNode.parentNode;
			var id = parent.querySelector('#id_annotation_number').value;
			var annotations = this.annotationData;
			annotations[id]['fields'][target.name] = target.value;
			this.annotationData = annotations;
		}
	}, {
		key: 'index',
		get: function get() {
			return this._index;
		},
		set: function set(index) {
			this._index = index;
		}
	}, {
		key: 'annotationData',
		get: function get() {
			return this._annotationData;
		},
		set: function set(data) {
			this._annotationData = data;
			this.annotationsField.val(JSON.stringify(data));
		}
	}]);

	return AnnotatedImageEditHandler;
}();