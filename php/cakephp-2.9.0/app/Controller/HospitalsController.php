<?php
App::uses('AppController', 'Controller');
/**
 * Hospitals Controller
 *
 * @property Hospital $Hospital
 * @property PaginatorComponent $Paginator
 */
class HospitalsController extends AppController {

/**
 * Components
 *
 * @var array
 */
	// public $components = array('Paginator');

/**
 * index method
 *
 * @return void
 */
	public function index() {
		$this->Hospital->recursive = 0;
		$this->set('hospitals', $this->Paginator->paginate());

	}

/**
 * view method
 *
 * @throws NotFoundException
 * @param string $id
 * @return void
 */
	public function view($id = null) {
		if (!$this->Hospital->exists($id)) {
			throw new NotFoundException(__('Invalid hospital'));
		}
		$options = array('conditions' => array('Hospital.' . $this->Hospital->primaryKey => $id));
		$this->set('hospital', $this->Hospital->find('first', $options));
	}

/**
 * add method
 *
 * @return void
 */
	public function add() {
		if ($this->request->is('post')) {
			$this->Hospital->create();
			if ($this->Hospital->save($this->request->data)) {
				$this->Flash->success(__('The hospital has been saved.'));
				return $this->redirect(array('action' => 'index'));
			} else {
				$this->Flash->error(__('The hospital could not be saved. Please, try again.'));
			}
		}
	}

/**
 * edit method
 *
 * @throws NotFoundException
 * @param string $id
 * @return void
 */
	public function edit($id = null) {
		if (!$this->Hospital->exists($id)) {
			throw new NotFoundException(__('Invalid hospital'));
		}
		if ($this->request->is(array('post', 'put'))) {
			if ($this->Hospital->save($this->request->data)) {
				$this->Flash->success(__('The hospital has been saved.'));
				return $this->redirect(array('action' => 'index'));
			} else {
				$this->Flash->error(__('The hospital could not be saved. Please, try again.'));
			}
		} else {
			$options = array('conditions' => array('Hospital.' . $this->Hospital->primaryKey => $id));
			$this->request->data = $this->Hospital->find('first', $options);
		}
	}

/**
 * delete method
 *
 * @throws NotFoundException
 * @param string $id
 * @return void
 */
	public function delete($id = null) {
		$this->Hospital->id = $id;
		if (!$this->Hospital->exists()) {
			throw new NotFoundException(__('Invalid hospital'));
		}
		$this->request->allowMethod('post', 'delete');
		if ($this->Hospital->delete()) {
			$this->Flash->success(__('The hospital has been deleted.'));
		} else {
			$this->Flash->error(__('The hospital could not be deleted. Please, try again.'));
		}
		return $this->redirect(array('action' => 'index'));
	}
}
