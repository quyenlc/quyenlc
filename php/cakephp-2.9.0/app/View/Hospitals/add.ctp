<div class="hospitals form">
<?php echo $this->Form->create('Hospital'); ?>
	<fieldset>
		<legend><?php echo __('Add Hospital'); ?></legend>
	<?php
		echo $this->Form->input('name');
		echo $this->Form->input('address');
	?>
	</fieldset>
<?php echo $this->Form->end(__('Submit')); ?>
</div>
<div class="actions">
	<h3><?php echo __('Actions'); ?></h3>
	<ul>

		<li><?php echo $this->Html->link(__('List Hospitals'), array('action' => 'index')); ?></li>
	</ul>
</div>
