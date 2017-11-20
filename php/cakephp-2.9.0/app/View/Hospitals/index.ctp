<div class="hospitals index">
	<h2><?php echo __('Hospitals'); ?></h2>
	<table cellpadding="0" cellspacing="0">
	<thead>
	<tr>
			<!-- <th><?php echo $this->Paginator->sort('id'); ?></th> -->
			<th> <div style="white-space:nowrap">
				<?php echo $this->Paginator->sort('name'); echo $this->TwitterBootstrap->search('name');?>
			</div></th>
			<th><?php echo $this->Paginator->sort('address'); echo $this->TwitterBootstrap->search('address');?></th>
			<th><?php echo $this->Paginator->sort('created'); ?></th>
			<th><?php echo $this->Paginator->sort('modified'); echo $this->TwitterBootstrap->search('');?></th>
			<th class="actions"><?php echo __('Actions'); ?></th>
	</tr>
	</thead>
	<tbody>
	<?php 
		foreach ($hospitals as $hospital): 
	?>
	<tr>
		<!-- <td><?php echo h($hospital['Hospital']['id']); ?>&nbsp;</td> -->
		<td><?php echo $hospital['Hospital']['name']; ?>&nbsp;</td>
		<td><?php echo $hospital['Hospital']['address']; ?>&nbsp;</td>
		<td><?php echo $hospital['Hospital']['created']; ?>&nbsp;</td>
		<td><?php echo $hospital['Hospital']['modified']; ?>&nbsp;</td>
		<td class="actions">
			<?php echo $this->Html->link(__('View'), array('action' => 'view', $hospital['Hospital']['id'])); ?>
			<?php echo $this->Html->link(__('Edit'), array('action' => 'edit', $hospital['Hospital']['id'])); ?>
			<?php echo $this->Form->postLink(__('Delete'), array('action' => 'delete', $hospital['Hospital']['id']), array('confirm' => __('Are you sure you want to delete # %s?', $hospital['Hospital']['id']))); ?>
		</td>
	</tr>
<?php endforeach; ?>
	</tbody>
	</table>
	<p>
	<?php
	echo $this->Paginator->counter(array(
		'format' => __('Page {:page} of {:pages}, showing {:current} records out of {:count} total, starting on record {:start}, ending on {:end}')
	));
	?>	</p>
	<div class="paging">
	<?php
		echo $this->Paginator->prev('< ' . __('previous'), array(), null, array('class' => 'prev disabled'));
		echo $this->Paginator->numbers(array('separator' => ''));
		echo $this->Paginator->next(__('next') . ' >', array(), null, array('class' => 'next disabled'));
	?>
	</div>
</div>
<div class="actions">
	<h3><?php echo __('Actions'); ?></h3>
	<ul>
		<li><?php echo $this->Html->link(__('New Hospital'), array('action' => 'add')); ?></li>
	</ul>
</div>
