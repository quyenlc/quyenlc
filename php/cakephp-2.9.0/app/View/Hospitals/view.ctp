<div class="hospitals view">
<h2><?php echo __('Hospital'); ?></h2>
	<dl>
		<dt><?php echo __('Id'); ?></dt>
		<dd>
			<?php echo h($hospital['Hospital']['id']); ?>
			&nbsp;
		</dd>
		<dt><?php echo __('Name'); ?></dt>
		<dd>
			<?php echo h($hospital['Hospital']['name']); ?>
			&nbsp;
		</dd>
		<dt><?php echo __('Address'); ?></dt>
		<dd>
			<?php echo h($hospital['Hospital']['address']); ?>
			&nbsp;
		</dd>
		<dt><?php echo __('Created'); ?></dt>
		<dd>
			<?php echo h($hospital['Hospital']['created']); ?>
			&nbsp;
		</dd>
		<dt><?php echo __('Modified'); ?></dt>
		<dd>
			<?php echo h($hospital['Hospital']['modified']); ?>
			&nbsp;
		</dd>
	</dl>
</div>
<div class="actions">
	<h3><?php echo __('Actions'); ?></h3>
	<ul>
		<li><?php echo $this->Html->link(__('Edit Hospital'), array('action' => 'edit', $hospital['Hospital']['id'])); ?> </li>
		<li><?php echo $this->Form->postLink(__('Delete Hospital'), array('action' => 'delete', $hospital['Hospital']['id']), array('confirm' => __('Are you sure you want to delete # %s?', $hospital['Hospital']['id']))); ?> </li>
		<li><?php echo $this->Html->link(__('List Hospitals'), array('action' => 'index')); ?> </li>
		<li><?php echo $this->Html->link(__('New Hospital'), array('action' => 'add')); ?> </li>
	</ul>
</div>
